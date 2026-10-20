# FitCoach (iOS)

A SwiftUI fitness-coaching app that combines the two sides of the market:

- **Professional side** (MFIT-style): client roster, assessments/anamnesis,
  remote workout prescription (dates, loads, rest, sets), exercise library, and
  a live view of client feedback.
- **Client side** (Prime App-style): today's workouts, per-set execution and
  feedback (reps/load/RPE/notes), and the diet plan — with coach edits appearing
  immediately.

Both roles share a single source of truth (`AppStore`), so a set the client
reports shows up on the coach's screen without any sync step.

> Built from the public functional description of those products, not from their
> binaries. The code here is original.

## Project layout

```
Sources/FitCoach/
  Models/Domain.swift        Person, Exercise, Workout, Set + feedback, Diet, Assessment
  Store/AppStore.swift       In-memory store (swap method bodies for your backend)
  FitCoachApp.swift          App entry point
  Views/
    RootView.swift           Role-based routing + account switcher
    Professional/            Coach: roster, client detail, prescribe workout
    Client/                  Client: today, workout detail + feedback, diet
    Shared/                  Reusable UI
Tests/AppStoreTests.swift    Unit tests for the store/domain
project.yml                  XcodeGen spec
```

## Build (requires macOS + Xcode)

This repository holds source only; an iOS app must be built on a Mac.

```bash
brew install xcodegen          # once
cd apps/fitcoach-ios
xcodegen generate              # creates FitCoach.xcodeproj
open FitCoach.xcodeproj        # run on the Simulator with ⌘R
```

Minimum: Xcode 15, iOS 17 deployment target.

## Current state

- End-to-end working UI for both roles against seeded mock data.
- The store is in memory: data resets on relaunch. The next step is a real
  backend — replace the method bodies in `AppStore` with network calls; the view
  layer does not change.
- Not yet built: real authentication, push notifications, payments, the AI
  workout generator (the `Store` is where those hook in).

## Publishing to the App Store

Publishing is done with **your** Apple Developer account on a Mac — it cannot be
done from this environment. Outline:

1. Enroll in the Apple Developer Program (US$99/year).
2. In Xcode, set a unique bundle identifier and your signing team
   (Signing & Capabilities).
3. Create the app record in App Store Connect (name, category: Health & Fitness,
   privacy details).
4. `Product ▸ Archive`, then distribute to App Store Connect.
5. Submit for review with screenshots and a privacy policy.

A note on the trade you asked about: for App Store review and legally, build the
product from your own requirements (as this code does). Copying a competitor's
screens, assets, or decompiled implementation invites both rejection and legal
exposure.
