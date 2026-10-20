import SwiftUI

/// Generate a draft training plan with the AI generator, then review it before
/// it reaches the client. The coach sets the goal, weekly frequency, and which
/// muscle groups to avoid (prefilled from the client's assessment), generates,
/// trims any session they don't want, and confirms. Nothing is saved until the
/// coach taps "Adicionar".
struct GenerateWorkoutView: View {
    @EnvironmentObject private var store: AppStore
    @Environment(\.dismiss) private var dismiss
    let client: Person

    @State private var request: WorkoutPlanRequest
    @State private var drafts: [Workout] = []
    @State private var isGenerating = false
    @State private var hasGenerated = false

    init(client: Person, assessment: Assessment?) {
        self.client = client
        _request = State(initialValue: WorkoutPlanRequest(prefilledFrom: assessment))
    }

    private var muscleGroups: [String] {
        Array(Set(store.exercises.map(\.muscleGroup))).sorted()
    }

    var body: some View {
        NavigationStack {
            Form {
                configSection
                generateSection
                if hasGenerated { reviewSection }
            }
            .navigationTitle("Gerar com IA")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) { Button("Cancelar") { dismiss() } }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Adicionar") { accept() }.disabled(drafts.isEmpty)
                }
            }
        }
    }

    private var configSection: some View {
        Section("Parâmetros") {
            Picker("Objetivo", selection: $request.goal) {
                ForEach(TrainingGoal.allCases) { goal in
                    Text(goal.title).tag(goal)
                }
            }
            Stepper("Treinos por semana: \(request.daysPerWeek)", value: $request.daysPerWeek, in: 1...6)
            DatePicker("Início", selection: $request.startDate, displayedComponents: .date)
        }
    }

    private var avoidSection: some View {
        Section("Evitar grupos musculares") {
            ForEach(muscleGroups, id: \.self) { group in
                Toggle(group, isOn: Binding(
                    get: { request.avoidedMuscleGroups.contains(group) },
                    set: { avoid in
                        if avoid {
                            if !request.avoidedMuscleGroups.contains(group) {
                                request.avoidedMuscleGroups.append(group)
                            }
                        } else {
                            request.avoidedMuscleGroups.removeAll { $0 == group }
                        }
                    }
                ))
            }
        }
    }

    @ViewBuilder
    private var generateSection: some View {
        avoidSection
        Section {
            Button {
                generate()
            } label: {
                HStack {
                    Spacer()
                    if isGenerating {
                        ProgressView()
                    } else {
                        Label(hasGenerated ? "Gerar novamente" : "Gerar plano",
                              systemImage: "wand.and.stars")
                    }
                    Spacer()
                }
            }
            .disabled(isGenerating)
        }
    }

    @ViewBuilder
    private var reviewSection: some View {
        if drafts.isEmpty {
            Section {
                Text("Nenhum treino gerado — todos os grupos musculares disponíveis foram evitados. Ajuste os parâmetros e gere novamente.")
                    .font(.callout)
                    .foregroundStyle(.secondary)
            }
        } else {
            Section("Plano gerado — revise antes de adicionar") {
                ForEach(drafts) { workout in
                    VStack(alignment: .leading, spacing: 6) {
                        Text(workout.title).font(.headline)
                        Text(workout.date.shortLabel).font(.caption).foregroundStyle(.secondary)
                        ForEach(workout.exercises) { we in
                            HStack {
                                Text(we.exercise.name)
                                Spacer()
                                Text(Self.setSummary(we))
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .padding(.vertical, 2)
                }
                .onDelete { drafts.remove(atOffsets: $0) }
            }
        }
    }

    /// Compact "4×10 · 30 kg · 75s" line for a generated exercise, whose sets all
    /// share the same scheme.
    private static func setSummary(_ we: WorkoutExercise) -> String {
        guard let first = we.sets.first else { return "" }
        return "\(we.sets.count)×\(first.targetReps) · \(Int(first.targetLoadKg)) kg · \(first.restSeconds)s"
    }

    private func generate() {
        Task {
            isGenerating = true
            drafts = await store.generateWorkoutPlan(for: client, request: request)
            hasGenerated = true
            isGenerating = false
        }
    }

    private func accept() {
        for workout in drafts { store.addWorkout(workout) }
        dismiss()
    }
}
