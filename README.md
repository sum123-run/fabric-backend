# Fabric App — Frontend

A React Native (Expo) app for fabric detection, virtual try-on, and outfit styling. Users can browse garment categories (Frocks, Saree, Kurta, and more), preview fabrics and styles, and see AI-generated try-on results.

## Demo

![App Demo](https://github.com/user-attachments/assets/64f748b0-75ba-4668-a642-26dce1ac00f6)
## Features

- 🧵 **Fabric Detection** — identifies fabric type from an image with a confidence score
- 📂 **Category Browsing** — Frocks, Saree, Kurta, and more, with style previews
- 🔐 **Authentication** — user login/signup (Firebase Auth)
- ⭐ **Feedback** — users can rate and submit feedback on outfit combinations

## Tech Stack

- **Framework:** React Native (Expo)
- **Auth & Backend services:** Firebase
- **Navigation:** Expo Router

## Screens

| Screen | Description |
|---|---|
| `SplashScreen` | App launch screen |
| `LoginScreen` / `SignupScreen` | User authentication |
| `LoadingScreen` | Loading state while processing |
| `PredictionScreen` | Fabric detection & try-on results |
| `AppScreenPreview` | Preview of generated outfit/fabric |

## Getting Started

```bash
# Clone the repo
git clone https://github.com/sum123-run/fabric-frontend.git
cd fabric-frontend

# Install dependencies
npm install

# Start the app
npx expo start
```

## Related Repos

- Frontend: [https://github.com/sum123-run/fabric-frontend/tree/main]

## License

[MIT]
