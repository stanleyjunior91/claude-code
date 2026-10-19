import SwiftUI

/// Client side — the Prime App-style experience: today's workout, the diet,
/// and a simple way to report each set as it's done.
struct ClientHomeView: View {
    @EnvironmentObject private var store: AppStore

    var body: some View {
        TabView {
            NavigationStack { TodayView() }
                .tabItem { Label("Treino", systemImage: "figure.strengthtraining.traditional") }
            NavigationStack { ClientDietView() }
                .tabItem { Label("Dieta", systemImage: "fork.knife") }
        }
    }
}

struct TodayView: View {
    @EnvironmentObject private var store: AppStore

    private var mine: [Workout] { store.workouts(for: store.currentUser) }

    var body: some View {
        List {
            ForEach(mine) { workout in
                Section {
                    NavigationLink(value: workout) {
                        VStack(alignment: .leading) {
                            Text(workout.title).font(.headline)
                            Text(workout.date.shortLabel).font(.caption).foregroundStyle(.secondary)
                        }
                    }
                } header: {
                    Text(workout.isComplete ? "Concluído" : "Pendente")
                }
            }
        }
        .navigationTitle("Meus treinos")
        .navigationDestination(for: Workout.self) { WorkoutDetailView(workoutID: $0.id) }
        .toolbar { ToolbarItem(placement: .topBarTrailing) { AccountSwitcher() } }
        .overlay {
            if mine.isEmpty {
                ContentUnavailableView("Sem treinos", systemImage: "calendar",
                                       description: Text("Seu personal ainda não prescreveu nada."))
            }
        }
    }
}

struct ClientDietView: View {
    @EnvironmentObject private var store: AppStore

    var body: some View {
        List {
            if let diet = store.diet(for: store.currentUser) {
                Section("Total diário") {
                    StatTile(label: "Calorias", value: "\(diet.totalKcal) kcal")
                }
                ForEach(diet.meals) { meal in
                    Section("\(meal.time) · \(meal.name)") {
                        ForEach(meal.items, id: \.self) { Text($0) }
                        Text("\(meal.kcal) kcal").font(.caption).foregroundStyle(.secondary)
                    }
                }
            } else {
                ContentUnavailableView("Sem dieta", systemImage: "fork.knife")
            }
        }
        .navigationTitle("Minha dieta")
    }
}
