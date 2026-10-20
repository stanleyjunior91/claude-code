import XCTest
@testable import FitCoach

@MainActor
final class AppStoreTests: XCTestCase {
    func testSeedsCoachWithClients() {
        let store = AppStore()
        XCTAssertEqual(store.currentUser.role, .professional)
        XCTAssertFalse(store.clients(of: store.currentUser).isEmpty)
    }

    func testFeedbackPropagatesToWorkout() {
        let store = AppStore()
        let client = store.clients.first { !store.workouts(for: $0).isEmpty }!
        let workout = store.workouts(for: client).first!
        let we = workout.exercises.first!
        let set = we.sets.first!

        store.recordFeedback(
            SetFeedback(completedReps: 10, usedLoadKg: 62, rpe: 8, note: "ok"),
            workoutID: workout.id, exerciseID: we.id, setID: set.id
        )

        let updated = store.workouts.first { $0.id == workout.id }!
        let updatedSet = updated.exercises.first!.sets.first { $0.id == set.id }!
        XCTAssertEqual(updatedSet.feedback?.completedReps, 10)
        XCTAssertEqual(updatedSet.feedback?.rpe, 8)
    }

    func testBMICalculation() {
        let a = Assessment(clientID: UUID(), date: Date(), weightKg: 80, heightCm: 200, answers: [:])
        XCTAssertEqual(a.bmi, 20, accuracy: 0.001)
    }

    // MARK: - AI workout generator

    func testGenerateProducesRequestedNumberOfSessions() async {
        let store = AppStore()
        let client = store.clients.first!
        let request = WorkoutPlanRequest(goal: .hypertrophy, daysPerWeek: 3, startDate: Date(), avoidedMuscleGroups: [])

        let plan = await store.generateWorkoutPlan(for: client, request: request)

        XCTAssertEqual(plan.count, 3)
        XCTAssertTrue(plan.allSatisfy { $0.clientID == client.id })
        XCTAssertTrue(plan.allSatisfy { !$0.exercises.isEmpty })
    }

    func testGenerateReturnsDraftsWithoutSaving() async {
        let store = AppStore()
        let client = store.clients.first!
        let before = store.workouts.count

        let plan = await store.generateWorkoutPlan(
            for: client,
            request: WorkoutPlanRequest(goal: .strength, daysPerWeek: 2, startDate: Date(), avoidedMuscleGroups: [])
        )

        XCTAssertEqual(store.workouts.count, before, "generation must not mutate the store")
        plan.forEach { store.addWorkout($0) }
        XCTAssertEqual(store.workouts.count, before + plan.count)
    }

    func testGoalDrivesSetAndRepScheme() async {
        let store = AppStore()
        let client = store.clients.first!

        let plan = await store.generateWorkoutPlan(
            for: client,
            request: WorkoutPlanRequest(goal: .strength, daysPerWeek: 3, startDate: Date(), avoidedMuscleGroups: [])
        )
        let set = plan.flatMap(\.exercises).flatMap(\.sets).first!
        XCTAssertEqual(set.targetReps, 5)
        XCTAssertEqual(set.restSeconds, 150)
        let exercise = plan.flatMap(\.exercises).first!
        XCTAssertEqual(exercise.sets.count, 5)
    }

    func testAvoidedMuscleGroupIsExcluded() async {
        let store = AppStore()
        let client = store.clients.first!

        let plan = await store.generateWorkoutPlan(
            for: client,
            request: WorkoutPlanRequest(goal: .hypertrophy, daysPerWeek: 6, startDate: Date(), avoidedMuscleGroups: ["Pernas"])
        )
        let groups = plan.flatMap(\.exercises).map(\.exercise.muscleGroup)
        XCTAssertFalse(groups.contains("Pernas"))
    }

    func testRequestPrefillFromAssessment() {
        let assessment = Assessment(
            clientID: UUID(), date: Date(), weightKg: 78, heightCm: 176,
            answers: ["Objetivo": "Hipertrofia", "Frequência semanal": "4x", "Lesões": "Dor no ombro"]
        )
        let request = WorkoutPlanRequest(prefilledFrom: assessment)

        XCTAssertEqual(request.goal, .hypertrophy)
        XCTAssertEqual(request.daysPerWeek, 4)
        XCTAssertEqual(request.avoidedMuscleGroups, ["Ombros"])
    }

    func testRequestPrefillDefaultsWhenNoAssessment() {
        let request = WorkoutPlanRequest(prefilledFrom: nil)
        XCTAssertEqual(request.goal, .hypertrophy)
        XCTAssertEqual(request.daysPerWeek, 3)
        XCTAssertTrue(request.avoidedMuscleGroups.isEmpty)
    }

    func testSessionsAreSpacedAcrossTheWeek() {
        let start = Calendar.current.startOfDay(for: Date())
        let dates = WorkoutGenerator.distributeDates(count: 3, from: start)
        let offsets = dates.map { Calendar.current.dateComponents([.day], from: start, to: $0).day! }
        XCTAssertEqual(offsets, [0, 2, 4])
    }
}
