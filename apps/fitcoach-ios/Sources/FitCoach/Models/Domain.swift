import Foundation

// MARK: - Roles

/// The two sides of the platform. A single person can hold only one role per
/// account, but the same data model serves both so the professional sees exactly
/// what the client sees.
enum Role: String, Codable, CaseIterable, Identifiable {
    case professional
    case client

    var id: String { rawValue }

    var title: String {
        switch self {
        case .professional: return "Profissional"
        case .client: return "Aluno"
        }
    }
}

// MARK: - People

struct Person: Identifiable, Codable, Hashable {
    let id: UUID
    var name: String
    var role: Role
    var email: String
    /// For a client, the professional who coaches them. Nil for professionals.
    var coachID: UUID?

    init(id: UUID = UUID(), name: String, role: Role, email: String, coachID: UUID? = nil) {
        self.id = id
        self.name = name
        self.role = role
        self.email = email
        self.coachID = coachID
    }
}

// MARK: - Exercise library

/// A reusable exercise definition from the shared library (the "1,800 videos"
/// idea from MFIT, here modelled as a catalogue the professional draws from).
struct Exercise: Identifiable, Codable, Hashable {
    let id: UUID
    var name: String
    var muscleGroup: String
    var demoVideoURL: URL?

    init(id: UUID = UUID(), name: String, muscleGroup: String, demoVideoURL: URL? = nil) {
        self.id = id
        self.name = name
        self.muscleGroup = muscleGroup
        self.demoVideoURL = demoVideoURL
    }
}

// MARK: - Prescribed training

/// One prescribed set of an exercise. `targetReps`/`targetLoad` are what the
/// professional assigns; `feedback` is what the client reports back per set —
/// the per-set feedback loop from Prime App.
struct ExerciseSet: Identifiable, Codable, Hashable {
    let id: UUID
    var order: Int
    var targetReps: Int
    var targetLoadKg: Double
    var restSeconds: Int
    var feedback: SetFeedback?

    init(id: UUID = UUID(), order: Int, targetReps: Int, targetLoadKg: Double, restSeconds: Int, feedback: SetFeedback? = nil) {
        self.id = id
        self.order = order
        self.targetReps = targetReps
        self.targetLoadKg = targetLoadKg
        self.restSeconds = restSeconds
        self.feedback = feedback
    }
}

/// What the client reports after performing a set.
struct SetFeedback: Codable, Hashable {
    var completedReps: Int
    var usedLoadKg: Double
    /// Rating of Perceived Exertion, 1...10.
    var rpe: Int
    var note: String
}

struct WorkoutExercise: Identifiable, Codable, Hashable {
    let id: UUID
    var exercise: Exercise
    var sets: [ExerciseSet]

    init(id: UUID = UUID(), exercise: Exercise, sets: [ExerciseSet]) {
        self.id = id
        self.exercise = exercise
        self.sets = sets
    }
}

/// A workout assigned to a client for a specific date. Edits by the
/// professional are reflected immediately for the client (single source of
/// truth in the store).
struct Workout: Identifiable, Codable, Hashable {
    let id: UUID
    var title: String
    var date: Date
    var clientID: UUID
    var exercises: [WorkoutExercise]

    init(id: UUID = UUID(), title: String, date: Date, clientID: UUID, exercises: [WorkoutExercise]) {
        self.id = id
        self.title = title
        self.date = date
        self.clientID = clientID
        self.exercises = exercises
    }

    var isComplete: Bool {
        exercises.allSatisfy { ex in ex.sets.allSatisfy { $0.feedback != nil } }
    }
}

// MARK: - Nutrition

struct Meal: Identifiable, Codable, Hashable {
    let id: UUID
    var name: String
    var time: String
    var items: [String]
    var kcal: Int

    init(id: UUID = UUID(), name: String, time: String, items: [String], kcal: Int) {
        self.id = id
        self.name = name
        self.time = time
        self.items = items
        self.kcal = kcal
    }
}

struct DietPlan: Identifiable, Codable, Hashable {
    let id: UUID
    var clientID: UUID
    var meals: [Meal]

    init(id: UUID = UUID(), clientID: UUID, meals: [Meal]) {
        self.id = id
        self.clientID = clientID
        self.meals = meals
    }

    var totalKcal: Int { meals.reduce(0) { $0 + $1.kcal } }
}

// MARK: - Assessment / anamnesis

/// A simple questionnaire-based assessment (the anamnese/avaliação idea from
/// MFIT). Kept generic: a list of question/answer pairs plus body metrics.
struct Assessment: Identifiable, Codable, Hashable {
    let id: UUID
    var clientID: UUID
    var date: Date
    var weightKg: Double
    var heightCm: Double
    var answers: [String: String]

    init(id: UUID = UUID(), clientID: UUID, date: Date, weightKg: Double, heightCm: Double, answers: [String: String]) {
        self.id = id
        self.clientID = clientID
        self.date = date
        self.weightKg = weightKg
        self.heightCm = heightCm
        self.answers = answers
    }

    var bmi: Double {
        guard heightCm > 0 else { return 0 }
        let m = heightCm / 100
        return weightKg / (m * m)
    }
}
