import Foundation
import Combine

/// In-memory store that acts as the single source of truth for both roles.
///
/// This is deliberately a mock: it seeds sample data and keeps everything in
/// memory so the UI runs end to end with no backend. Swap the method bodies for
/// network calls (REST/GraphQL) when the backend exists — the view layer does
/// not need to change because it only talks to this store.
@MainActor
final class AppStore: ObservableObject {
    @Published private(set) var people: [Person] = []
    @Published private(set) var exercises: [Exercise] = []
    @Published private(set) var workouts: [Workout] = []
    @Published private(set) var diets: [DietPlan] = []
    @Published private(set) var assessments: [Assessment] = []

    /// Who is currently signed in. Switching this flips the whole UI between
    /// the professional and client experiences.
    @Published var currentUser: Person

    init() {
        let coach = Person(name: "Ana Personal", role: .professional, email: "ana@fitcoach.app")
        let client1 = Person(name: "Bruno Aluno", role: .client, email: "bruno@email.com", coachID: coach.id)
        let client2 = Person(name: "Carla Aluna", role: .client, email: "carla@email.com", coachID: coach.id)

        let library = Self.seedExercises()
        self.people = [coach, client1, client2]
        self.exercises = library
        self.currentUser = coach
        self.workouts = Self.seedWorkouts(for: client1, library: library)
        self.diets = [Self.seedDiet(for: client1)]
        self.assessments = [Self.seedAssessment(for: client1)]
    }

    // MARK: - Queries

    var clients: [Person] { people.filter { $0.role == .client } }

    func clients(of coach: Person) -> [Person] {
        people.filter { $0.role == .client && $0.coachID == coach.id }
    }

    func workouts(for client: Person) -> [Workout] {
        workouts.filter { $0.clientID == client.id }.sorted { $0.date < $1.date }
    }

    func diet(for client: Person) -> DietPlan? {
        diets.first { $0.clientID == client.id }
    }

    func latestAssessment(for client: Person) -> Assessment? {
        assessments.filter { $0.clientID == client.id }.sorted { $0.date > $1.date }.first
    }

    func person(_ id: UUID) -> Person? { people.first { $0.id == id } }

    // MARK: - Mutations (professional)

    func addWorkout(_ workout: Workout) {
        workouts.append(workout)
    }

    func updateWorkout(_ workout: Workout) {
        guard let idx = workouts.firstIndex(where: { $0.id == workout.id }) else { return }
        workouts[idx] = workout
    }

    func upsertDiet(_ diet: DietPlan) {
        if let idx = diets.firstIndex(where: { $0.clientID == diet.clientID }) {
            diets[idx] = diet
        } else {
            diets.append(diet)
        }
    }

    // MARK: - AI workout generator

    /// Produce a draft training plan for a client from the coach's request.
    ///
    /// This is the seam where a real model/backend call goes: send the client's
    /// assessment plus the request, receive the workouts. Today it runs a local
    /// rule-based engine (`WorkoutGenerator`) so the feature works end to end
    /// with no backend — swap this body for a network/LLM call without touching
    /// the views. The returned workouts are *drafts*: the professional reviews
    /// and trims them, then saves the ones they want via `addWorkout`.
    func generateWorkoutPlan(for client: Person, request: WorkoutPlanRequest) async -> [Workout] {
        let generator = WorkoutGenerator(library: exercises, clientID: client.id, request: request)
        return generator.makePlan()
    }

    // MARK: - Mutations (client)

    /// Record per-set feedback. Because the store is shared, the professional
    /// sees this immediately on their side.
    func recordFeedback(_ feedback: SetFeedback, workoutID: UUID, exerciseID: UUID, setID: UUID) {
        guard let wIdx = workouts.firstIndex(where: { $0.id == workoutID }),
              let eIdx = workouts[wIdx].exercises.firstIndex(where: { $0.id == exerciseID }),
              let sIdx = workouts[wIdx].exercises[eIdx].sets.firstIndex(where: { $0.id == setID })
        else { return }
        workouts[wIdx].exercises[eIdx].sets[sIdx].feedback = feedback
    }

    // MARK: - Seed data

    private static func seedExercises() -> [Exercise] {
        [
            Exercise(name: "Agachamento livre", muscleGroup: "Pernas"),
            Exercise(name: "Supino reto", muscleGroup: "Peito"),
            Exercise(name: "Remada curvada", muscleGroup: "Costas"),
            Exercise(name: "Desenvolvimento militar", muscleGroup: "Ombros"),
            Exercise(name: "Rosca direta", muscleGroup: "Bíceps"),
            Exercise(name: "Tríceps corda", muscleGroup: "Tríceps"),
        ]
    }

    private static func seedWorkouts(for client: Person, library: [Exercise]) -> [Workout] {
        func sets(_ n: Int, reps: Int, load: Double, rest: Int) -> [ExerciseSet] {
            (1...n).map { ExerciseSet(order: $0, targetReps: reps, targetLoadKg: load, restSeconds: rest) }
        }
        let today = Calendar.current.startOfDay(for: Date())
        return [
            Workout(
                title: "Treino A — Membros inferiores",
                date: today,
                clientID: client.id,
                exercises: [
                    WorkoutExercise(exercise: library[0], sets: sets(4, reps: 10, load: 60, rest: 90)),
                    WorkoutExercise(exercise: library[3], sets: sets(3, reps: 12, load: 20, rest: 60)),
                ]
            ),
            Workout(
                title: "Treino B — Membros superiores",
                date: Calendar.current.date(byAdding: .day, value: 1, to: today)!,
                clientID: client.id,
                exercises: [
                    WorkoutExercise(exercise: library[1], sets: sets(4, reps: 8, load: 50, rest: 120)),
                    WorkoutExercise(exercise: library[2], sets: sets(4, reps: 10, load: 40, rest: 90)),
                ]
            ),
        ]
    }

    private static func seedDiet(for client: Person) -> DietPlan {
        DietPlan(clientID: client.id, meals: [
            Meal(name: "Café da manhã", time: "07:00", items: ["Ovos", "Aveia", "Fruta"], kcal: 450),
            Meal(name: "Almoço", time: "12:30", items: ["Arroz", "Frango", "Salada"], kcal: 700),
            Meal(name: "Lanche", time: "16:00", items: ["Iogurte", "Castanhas"], kcal: 300),
            Meal(name: "Jantar", time: "20:00", items: ["Batata-doce", "Carne", "Legumes"], kcal: 650),
        ])
    }

    private static func seedAssessment(for client: Person) -> Assessment {
        Assessment(
            clientID: client.id,
            date: Date(),
            weightKg: 78,
            heightCm: 176,
            answers: [
                "Objetivo": "Hipertrofia",
                "Frequência semanal": "4x",
                "Lesões": "Nenhuma",
            ]
        )
    }
}
