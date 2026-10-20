import Foundation

// MARK: - Training goal

/// The coach's target for a client. Each goal maps to a concrete prescription
/// (set/rep scheme, rest, and a starting-load factor) grounded in common
/// training practice. The enum is the single place those parameters live, so
/// the generator and any future tuning stay consistent.
enum TrainingGoal: String, Codable, CaseIterable, Identifiable {
    case hypertrophy
    case strength
    case endurance
    case generalFitness

    var id: String { rawValue }

    var title: String {
        switch self {
        case .hypertrophy: return "Hipertrofia"
        case .strength: return "Força"
        case .endurance: return "Resistência"
        case .generalFitness: return "Condicionamento geral"
        }
    }

    /// Set/rep/rest scheme plus a multiplier applied to a muscle group's base
    /// starting load. Loads are a conservative *starting* suggestion the coach
    /// tunes per client — the model has no 1RM data.
    struct Prescription {
        var sets: Int
        var reps: Int
        var restSeconds: Int
        var loadFactor: Double
    }

    var prescription: Prescription {
        switch self {
        case .strength: return Prescription(sets: 5, reps: 5, restSeconds: 150, loadFactor: 1.2)
        case .hypertrophy: return Prescription(sets: 4, reps: 10, restSeconds: 75, loadFactor: 1.0)
        case .generalFitness: return Prescription(sets: 3, reps: 12, restSeconds: 60, loadFactor: 0.8)
        case .endurance: return Prescription(sets: 3, reps: 18, restSeconds: 40, loadFactor: 0.6)
        }
    }

    /// Best-effort mapping from a free-text assessment answer (e.g. "Hipertrofia").
    init?(answerText: String?) {
        guard let text = answerText?.lowercased() else { return nil }
        if text.contains("hipertrofia") { self = .hypertrophy }
        else if text.contains("força") || text.contains("forca") { self = .strength }
        else if text.contains("resist") { self = .endurance }
        else if text.contains("condicion") || text.contains("geral") || text.contains("emagrec") { self = .generalFitness }
        else { return nil }
    }
}

// MARK: - Request

/// Everything the generator needs to produce a plan. Prefilled from the
/// client's latest assessment, then adjustable by the coach before generating.
struct WorkoutPlanRequest {
    var goal: TrainingGoal
    var daysPerWeek: Int
    var startDate: Date
    /// Muscle groups to leave out entirely (e.g. because of an injury).
    var avoidedMuscleGroups: [String]

    init(goal: TrainingGoal, daysPerWeek: Int, startDate: Date, avoidedMuscleGroups: [String]) {
        self.goal = goal
        self.daysPerWeek = daysPerWeek
        self.startDate = startDate
        self.avoidedMuscleGroups = avoidedMuscleGroups
    }
}

extension WorkoutPlanRequest {
    /// Seed a request from the anamnese: objective → goal, weekly frequency →
    /// days, reported injuries → avoided groups. Everything falls back to a safe
    /// default the coach can override.
    init(prefilledFrom assessment: Assessment?, startDate: Date = Date()) {
        let answers = assessment?.answers ?? [:]
        self.init(
            goal: TrainingGoal(answerText: answers["Objetivo"]) ?? .hypertrophy,
            daysPerWeek: Self.parseDays(answers["Frequência semanal"]) ?? 3,
            startDate: startDate,
            avoidedMuscleGroups: Self.parseInjuries(answers["Lesões"])
        )
    }

    /// Pull the first whole number out of a frequency answer like "4x" or
    /// "3 vezes", clamped to a sane weekly range.
    static func parseDays(_ answer: String?) -> Int? {
        guard let answer else { return nil }
        let runs = answer.components(separatedBy: CharacterSet.decimalDigits.inverted)
        guard let first = runs.first(where: { !$0.isEmpty }), let n = Int(first) else { return nil }
        return min(max(n, 1), 6)
    }

    /// Map injury text to the muscle groups worth avoiding. Deliberately coarse:
    /// the coach confirms the result in the UI. "Nenhuma" / empty → avoid nothing.
    static func parseInjuries(_ answer: String?) -> [String] {
        guard let answer, !answer.isEmpty else { return [] }
        let text = answer.lowercased()
        if text.contains("nenhum") { return [] }

        let rules: [(keywords: [String], group: String)] = [
            (["ombro", "manguito"], "Ombros"),
            (["joelho", "perna", "coxa", "quadríceps", "quadriceps", "posterior", "panturrilha"], "Pernas"),
            (["lombar", "coluna", "costas", "dorsal", "hérnia", "hernia"], "Costas"),
            (["peito", "peitoral"], "Peito"),
            (["cotovelo", "bíceps", "biceps"], "Bíceps"),
            (["punho", "tríceps", "triceps"], "Tríceps"),
        ]
        var groups: Set<String> = []
        for rule in rules where rule.keywords.contains(where: { text.contains($0) }) {
            groups.insert(rule.group)
        }
        return groups.sorted()
    }
}

// MARK: - Engine

/// Turns a `WorkoutPlanRequest` into a set of dated workouts drawn from the
/// exercise library. Pure value type with no side effects so it is easy to test
/// and so `AppStore` can wrap it behind an async seam (a future model/backend
/// call) without the views changing.
struct WorkoutGenerator {
    let library: [Exercise]
    let clientID: UUID
    let request: WorkoutPlanRequest

    /// At most this many exercises per session, keeping a generated day realistic.
    static let maxExercisesPerSession = 6

    /// Movement family an exercise belongs to, used to assemble splits.
    enum MuscleCategory {
        case push, pull, legs, other

        static func of(_ muscleGroup: String) -> MuscleCategory {
            switch muscleGroup.lowercased() {
            case "peito", "peitoral", "ombros", "ombro", "tríceps", "triceps": return .push
            case "costas", "dorsal", "bíceps", "biceps": return .pull
            case "pernas", "perna", "glúteos", "gluteos", "panturrilha": return .legs
            default: return .other
            }
        }
    }

    /// A session template: a label plus which categories it draws exercises from.
    private struct SessionSpec {
        let label: String
        let categories: Set<MuscleCategory>
    }

    func makePlan() -> [Workout] {
        let specs = Self.split(forDaysPerWeek: request.daysPerWeek)
        let dates = Self.distributeDates(count: specs.count, from: request.startDate)
        let scheme = request.goal.prescription
        let letters = Array("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        var workouts: [Workout] = []
        for (index, spec) in specs.enumerated() {
            let chosen = library.filter { exercise in
                spec.categories.contains(MuscleCategory.of(exercise.muscleGroup))
                    && !isAvoided(exercise.muscleGroup)
            }.prefix(Self.maxExercisesPerSession)

            guard !chosen.isEmpty else { continue }

            let exercises = chosen.map { exercise -> WorkoutExercise in
                let load = Self.roundToStep(Self.baseLoad(for: exercise.muscleGroup) * scheme.loadFactor)
                let sets = (1...scheme.sets).map { order in
                    ExerciseSet(order: order, targetReps: scheme.reps, targetLoadKg: load, restSeconds: scheme.restSeconds)
                }
                return WorkoutExercise(exercise: exercise, sets: sets)
            }

            let letter = String(letters[index % letters.count])
            workouts.append(Workout(
                title: "Treino \(letter) — \(spec.label)",
                date: dates[index],
                clientID: clientID,
                exercises: exercises
            ))
        }
        return workouts
    }

    private func isAvoided(_ group: String) -> Bool {
        request.avoidedMuscleGroups.contains { $0.caseInsensitiveCompare(group) == .orderedSame }
    }

    // MARK: Split templates

    private static func split(forDaysPerWeek days: Int) -> [SessionSpec] {
        let full = SessionSpec(label: "Corpo inteiro", categories: [.push, .pull, .legs, .other])
        let upper = SessionSpec(label: "Superiores", categories: [.push, .pull, .other])
        let lower = SessionSpec(label: "Inferiores", categories: [.legs])
        let push = SessionSpec(label: "Empurrar", categories: [.push])
        let pull = SessionSpec(label: "Puxar", categories: [.pull, .other])
        let legs = SessionSpec(label: "Pernas", categories: [.legs])

        switch min(max(days, 1), 6) {
        case 1: return [full]
        case 2: return [upper, lower]
        case 3: return [push, pull, legs]
        case 4: return [upper, lower, upper, lower]
        case 5: return [push, pull, legs, upper, lower]
        default: return [push, pull, legs, push, pull, legs]
        }
    }

    // MARK: Dates

    /// Spread `count` sessions across a 7-day week starting at `start`, so they
    /// land on spaced-out days rather than back to back.
    static func distributeDates(count: Int, from start: Date) -> [Date] {
        guard count > 0 else { return [] }
        let calendar = Calendar.current
        let day0 = calendar.startOfDay(for: start)
        return (0..<count).map { index in
            let offset = Int((Double(index) * 7.0 / Double(count)).rounded(.down))
            return calendar.date(byAdding: .day, value: offset, to: day0) ?? day0
        }
    }

    // MARK: Loads

    /// A modest starting load per muscle group, before the goal's factor. These
    /// are suggestions a coach adjusts, not prescriptions from measured strength.
    private static func baseLoad(for muscleGroup: String) -> Double {
        switch muscleGroup.lowercased() {
        case "pernas", "perna": return 40
        case "peito", "peitoral", "costas", "dorsal": return 30
        case "ombros", "ombro": return 20
        case "tríceps", "triceps": return 15
        case "bíceps", "biceps": return 12
        default: return 20
        }
    }

    static func roundToStep(_ value: Double, step: Double = 2.5) -> Double {
        (value / step).rounded() * step
    }
}
