# Hackapizza 🍕

## Overview

### Welcome, Challenger! 🌟

Congratulations! You have earned a place among the **top 10% of candidates** who made it through the selection process. This challenge is designed to test your **creativity, problem-solving skills, and technical expertise**.

However, with great talent comes great responsibility. This challenge **will not be easy**. It may seem complex at first glance, even overwhelming. It will demand **time, focus, and innovation**—even to fully grasp its scope.

But we know you don’t back down from a challenge. In fact, **true talent emerges in the face of adversity**. We are confident that you will prove yourself up to the task.

![Motivation](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2Fd4cd3a9d619dec67942e5344dcacf9e4%2F9gw32h.gif?generation=1737047022355670&alt=media)

## 📅 Challenge Timeline

- **Start Date:** January 18, 2025
- **End Date:** January 19, 2025

---

## 🌌 The Challenge 🪐

Welcome to **Cosmic Cycle 789**, where humanity has expanded beyond the limits of the known universe and into uncharted dimensions. In this vast and intricate reality, **gastronomy** has evolved into an art form that transcends both **space and time**.

Interdimensional restaurants flourish across the cosmos:

- Sushi bars on **Pandora** serve **Magikarp sashimi** and **Vaporeon dumplings**.
- Tatooine taverns infuse dishes with **Pipeweed** for an enhanced flavor experience.
- High-tech eateries craft sauces using the enigmatic **Slurm**, blending contrasting flavors into interstellar delights.

![Galactic Food](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2F888315aac2d2bdd249e8df8fc79f8043%2Fimage.png?generation=1737046855158236&alt=media)

However, with this expansion comes **new responsibilities**. The **Galactic Federation** strictly regulates ingredients, preparation methods, and certifications to ensure **culinary safety across species**. Chefs must navigate:

- Complex interdimensional regulations 📜
- Ingredients that exist in multiple quantum states simultaneously ⚛️
- Dietary restrictions for thousands of species across the **multiverse** 🌌

At the heart of this galactic cuisine is the **Cosmic Pizza**—a dish of **legendary proportions**. It is said that its mozzarella is crafted from the very essence of the **Milky Way**, and it requires the heat of three suns to bake. Some even worship it as a **divine entity**.

![Cosmic Pizza](<https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F6840884%2F0c07b3e6f34ac48b9bb627387ce71531%2FTesto%20del%20paragrafo%20(1).png?generation=1737047186767633&alt=media>)

---

## 💻 Technical Specifications

### Your Mission

Develop an **AI-powered assistant** to guide intergalactic travelers through the vast and exotic **culinary landscape of the cosmos**.

Your system must be able to:

✅ **Understand Natural Language Queries** – Users will ask for dish recommendations in **free-form text**.  
✅ **Handle Complex Queries** – Consider **preferences, dietary restrictions, and cultural nuances**.  
✅ **Process Multiple Data Sources** – Extract and process information from **menus, blogs, Galactic Federation laws, and cookbooks**.  
✅ **Ensure Compliance** – Verify dishes against **galactic regulations**.

### AI Capabilities

Your system should utilize **Generative AI** techniques, including:

- **Retrieval-Augmented Generation (RAG)**
- **AI Agents**
- **Multimodal Data Processing** (text, images, structured data)

The AI must be capable of:

- Receiving **natural language food requests**
- Returning **compliant and relevant dish recommendations** based on the given documentation

🛠 **Tech Stack:**  
This project is built using **FastAPI**, **LangChain**, **ChromaDB**, and other AI-related dependencies. The full list of dependencies is available in `pyproject.toml`.

---

## 🎯 Solution Architecture

The solution consists of three core components:

1. Entity Extraction & Knowledge Graph Storage
   The ingeston pipeline parses documents to extract key entities such as ingredients, dishes, planets, and culinary techniques. The structured data is stored in a Neo4j graph database, allowing efficient query execution.

2. A LangGraph-powered agent that generates and executes Cypher queries.
   Uses LLM-based reasoning to match user queries with structured graph data. The agent is empowered by a toolkit for accessing the Neo4j database, executing queries and returning parsed results.

3. Converts the query response into a structured output format.
   Maps dishes to their respective IDs and handles cases where no exact match is found in order to align with the requirements of the Kaggle evaluation system.

---

## Usage

The template is based on [UV](https://docs.astral.sh/) as package manager and [Just](https://github.com/casey/just) as command runner. You need to have both installed in your system to use this template.

Once you have those, you can just run

```bash
just dev-sync
```

### Formatting, Linting and Testing

You can configure Ruff by editing the `.ruff.toml` file. It is currently set to the default configuration.

Format your code:

```bash
just format
```

Run linters (ruff and mypy):

```bash
just lint
```
