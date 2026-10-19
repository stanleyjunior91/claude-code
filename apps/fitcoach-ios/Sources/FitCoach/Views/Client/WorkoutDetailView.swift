import SwiftUI

/// The per-set execution + feedback screen — the heart of the client side.
/// Reads the workout live from the store (by id) so coach edits appear here
/// immediately, and writes feedback straight back for the coach to see.
struct WorkoutDetailView: View {
    @EnvironmentObject private var store: AppStore
    let workoutID: UUID

    private var workout: Workout? { store.workouts.first { $0.id == workoutID } }

    var body: some View {
        if let workout {
            List {
                ForEach(workout.exercises) { we in
                    Section(we.exercise.muscleGroup + " · " + we.exercise.name) {
                        ForEach(we.sets.sorted(by: { $0.order < $1.order })) { set in
                            SetRow(workoutID: workout.id, exerciseID: we.id, set: set)
                        }
                    }
                }
            }
            .navigationTitle(workout.title)
        } else {
            ContentUnavailableView("Treino não encontrado", systemImage: "questionmark")
        }
    }
}

private struct SetRow: View {
    @EnvironmentObject private var store: AppStore
    let workoutID: UUID
    let exerciseID: UUID
    let set: ExerciseSet
    @State private var expanded = false

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("Série \(set.order)")
                Spacer()
                Text("\(set.targetReps) reps · \(Int(set.targetLoadKg)) kg · \(set.restSeconds)s")
                    .font(.caption).foregroundStyle(.secondary)
            }
            if let f = set.feedback {
                Label("\(f.completedReps) reps a \(Int(f.usedLoadKg)) kg · RPE \(f.rpe)",
                      systemImage: "checkmark.circle.fill")
                    .font(.caption).foregroundStyle(.green)
            } else {
                Button("Registrar série") { expanded = true }
                    .font(.caption)
            }
        }
        .sheet(isPresented: $expanded) {
            SetFeedbackForm(set: set) { feedback in
                store.recordFeedback(feedback, workoutID: workoutID, exerciseID: exerciseID, setID: set.id)
                expanded = false
            }
        }
    }
}

private struct SetFeedbackForm: View {
    @Environment(\.dismiss) private var dismiss
    let set: ExerciseSet
    let onSave: (SetFeedback) -> Void

    @State private var reps: Int
    @State private var load: Double
    @State private var rpe = 7
    @State private var note = ""

    init(set: ExerciseSet, onSave: @escaping (SetFeedback) -> Void) {
        self.set = set
        self.onSave = onSave
        _reps = State(initialValue: set.targetReps)
        _load = State(initialValue: set.targetLoadKg)
    }

    var body: some View {
        NavigationStack {
            Form {
                Stepper("Reps realizadas: \(reps)", value: $reps, in: 0...50)
                Stepper("Carga usada: \(Int(load)) kg", value: $load, in: 0...300, step: 2.5)
                Stepper("RPE (esforço): \(rpe)", value: $rpe, in: 1...10)
                TextField("Observação", text: $note, axis: .vertical)
            }
            .navigationTitle("Série \(set.order)")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) { Button("Cancelar") { dismiss() } }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Salvar") {
                        onSave(SetFeedback(completedReps: reps, usedLoadKg: load, rpe: rpe, note: note))
                    }
                }
            }
        }
    }
}
