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
}
