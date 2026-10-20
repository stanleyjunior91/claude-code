import SwiftUI

/// Build and assign a workout from the exercise library — dates, loads, rest,
/// and sets, like MFIT's remote prescription.
struct PrescribeWorkoutView: View {
    @EnvironmentObject private var store: AppStore
    @Environment(\.dismiss) private var dismiss
    let client: Person

    @State private var title = "Novo treino"
    @State private var date = Date()
    @State private var drafts: [Draft] = []

    struct Draft: Identifiable {
        let id = UUID()
        var exercise: Exercise
        var setCount = 3
        var reps = 10
        var load = 20.0
        var rest = 60
    }

    var body: some View {
        NavigationStack {
            Form {
                Section("Detalhes") {
                    TextField("Título", text: $title)
                    DatePicker("Data", selection: $date, displayedComponents: .date)
                }

                Section("Exercícios") {
                    ForEach($drafts) { $draft in
                        VStack(alignment: .leading) {
                            Text(draft.exercise.name).font(.headline)
                            Stepper("Séries: \(draft.setCount)", value: $draft.setCount, in: 1...8)
                            Stepper("Reps: \(draft.reps)", value: $draft.reps, in: 1...30)
                            Stepper("Carga: \(Int(draft.load)) kg", value: $draft.load, in: 0...300, step: 2.5)
                            Stepper("Descanso: \(draft.rest)s", value: $draft.rest, in: 15...240, step: 15)
                        }
                    }
                    Menu("Adicionar exercício") {
                        ForEach(store.exercises) { ex in
                            Button(ex.name) { drafts.append(Draft(exercise: ex)) }
                        }
                    }
                }
            }
            .navigationTitle("Prescrever")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) { Button("Cancelar") { dismiss() } }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Salvar") { save() }.disabled(drafts.isEmpty)
                }
            }
        }
    }

    private func save() {
        let exercises = drafts.map { draft in
            let sets = (1...draft.setCount).map {
                ExerciseSet(order: $0, targetReps: draft.reps, targetLoadKg: draft.load, restSeconds: draft.rest)
            }
            return WorkoutExercise(exercise: draft.exercise, sets: sets)
        }
        store.addWorkout(Workout(title: title, date: date, clientID: client.id, exercises: exercises))
        dismiss()
    }
}
