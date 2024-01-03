# Google Play Portfolio Scraper 🎮

A comprehensive tool to gather detailed information about games I've developed and published on the Google Play Store.

---

## Features

- **Icon**: Visual representation of each game.
- **App ID**: Unique identifier for each game.
- **Title**: Game titles for easy identification.
- **Genre**: Categorization of games by genre.
- **Installs**: Insights into the popularity and reach of each game.
- **Release Date**: Chronological overview of when each game was launched.
- **URL**: Direct links to the game's page on the Google Play Store.

---

## Overview

Contained within the file `apps.xlsx` is a comprehensive collection of games I've developed over the years. This serves as a detailed reference, showcasing various aspects of each game.

Please note: While some games may have been removed from the Google Play Store for various reasons, all the package identifiers can be found in the `packages` file.

---

## Getting Started

### Prerequisites

- Python installed on your machine.

### Setup Instructions

1. **Clone the Repository**: 
    ```
    git clone [repository-url]
    ```
2. **Update Package IDs**:
    - Navigate to the `packages` file.
    - Update the package identifiers as required.

3. **Run the Scraper**:
    ```
    python runner.py packages
    ```