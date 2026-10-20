import SwiftUI

/// Chooses the experience based on the signed-in role. A role switcher lives in
/// a toolbar so you can demo both sides without a login screen.
struct RootView: View {
    @EnvironmentObject private var store: AppStore

    var body: some View {
        Group {
            switch store.currentUser.role {
            case .professional:
                ProfessionalHomeView()
            case .client:
                ClientHomeView()
            }
        }
    }
}

/// A lightweight account picker used in place of real authentication for the
/// demo build. Replace with a proper sign-in flow against the backend.
struct AccountSwitcher: View {
    @EnvironmentObject private var store: AppStore

    var body: some View {
        Menu {
            ForEach(store.people) { person in
                Button {
                    store.currentUser = person
                } label: {
                    Label("\(person.name) · \(person.role.title)",
                          systemImage: person.id == store.currentUser.id ? "checkmark" : "person")
                }
            }
        } label: {
            Image(systemName: "person.crop.circle")
        }
    }
}
