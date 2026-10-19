import SwiftUI

/// Professional side — the MFIT-style coach experience: a roster of clients,
/// each drilling into their plan, assessment, and prescription tools.
struct ProfessionalHomeView: View {
    @EnvironmentObject private var store: AppStore

    var body: some View {
        NavigationStack {
            List {
                Section("Meus alunos") {
                    ForEach(store.clients(of: store.currentUser)) { client in
                        NavigationLink(value: client) {
                            VStack(alignment: .leading) {
                                Text(client.name)
                                Text(client.email).font(.caption).foregroundStyle(.secondary)
                            }
                        }
                    }
                }
            }
            .navigationTitle("FitCoach")
            .navigationDestination(for: Person.self) { ClientDetailView(client: $0) }
            .toolbar { ToolbarItem(placement: .topBarTrailing) { AccountSwitcher() } }
        }
    }
}

struct ClientDetailView: View {
    @EnvironmentObject private var store: AppStore
    let client: Person
    @State private var showingPrescribe = false

    var body: some View {
        List {
            if let a = store.latestAssessment(for: client) {
                Section("Avaliação") {
                    HStack {
                        StatTile(label: "Peso", value: "\(Int(a.weightKg)) kg")
                        StatTile(label: "IMC", value: String(format: "%.1f", a.bmi))
                    }
                    ForEach(a.answers.sorted(by: { $0.key < $1.key }), id: \.key) { k, v in
                        HStack { Text(k); Spacer(); Text(v).foregroundStyle(.secondary) }
                    }
                }
            }

            Section("Treinos prescritos") {
                ForEach(store.workouts(for: client)) { workout in
                    VStack(alignment: .leading, spacing: 4) {
                        HStack {
                            Text(workout.title)
                            Spacer()
                            if workout.isComplete {
                                Image(systemName: "checkmark.seal.fill").foregroundStyle(.green)
                            }
                        }
                        Text(workout.date.shortLabel).font(.caption).foregroundStyle(.secondary)
                        FeedbackSummary(workout: workout)
                    }
                }
            }

            if let diet = store.diet(for: client) {
                Section("Dieta — \(diet.totalKcal) kcal/dia") {
                    ForEach(diet.meals) { meal in
                        HStack {
                            Text("\(meal.time)  \(meal.name)")
                            Spacer()
                            Text("\(meal.kcal) kcal").foregroundStyle(.secondary)
                        }
                    }
                }
            }
        }
        .navigationTitle(client.name)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button { showingPrescribe = true } label: { Image(systemName: "plus") }
            }
        }
        .sheet(isPresented: $showingPrescribe) {
            PrescribeWorkoutView(client: client)
        }
    }
}

/// Shows how much of a workout the client has reported back on — the coach's
/// view into the per-set feedback.
private struct FeedbackSummary: View {
    let workout: Workout

    var body: some View {
        let total = workout.exercises.flatMap(\.sets).count
        let done = workout.exercises.flatMap(\.sets).filter { $0.feedback != nil }.count
        Text("\(done)/\(total) séries reportadas")
            .font(.caption2)
            .foregroundStyle(done == total ? .green : .secondary)
    }
}
