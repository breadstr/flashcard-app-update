## Flashcard Study Tool

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This Python script provides a command-line interface for creating, managing, studying, and editing flashcard decks. It allows users to organize their study material into decks of cards, each containing a question and an answer. The tool supports features like spaced repetition for studying, deck import/export, and various editing options.

## Features

Create Decks: Easily create new flashcard decks by providing a name and adding cards with questions and answers.
Select Decks: Choose from existing decks to study or edit.
Study Decks: Study cards using a basic spaced repetition algorithm. Cards reviewed incorrectly appear more frequently.
Edit Decks:
    Edit Cards: Modify the question or answer of existing cards.
    Sort Cards: Sort cards within a deck alphabetically by question or answer, or by the date they were created.
    Search Cards: Find specific cards by searching for a keyword in the question.
    Add Cards: Add new cards to an existing deck.
    Select Study Mode: Changes the current study mode.
Export Decks: Save a copy of a selected deck to a specified directory.
Import Decks: Load decks from `.csv` files into the application.

## Getting Started

### Prerequisites

* Python 3.x installed on your system.

### Installation

1.  Save the provided Python code as a `.py` file (e.g., `flashcards.py`).
2.  Create a directory named `Decks` in the same location as the Python script. This is where your decks will be stored by default.

### Running the Application

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved the `flashcards.py` file.
3.  Run the script using the command: `python flashcards.py`

## Usage

The application presents a menu with the following options:

1.  **Make Deck:** Guides you through the process of creating a new deck by entering a name and adding question-answer pairs.
2.  **Select Deck:** Lists the available decks in the `Decks` directory and allows you to choose one for studying or editing.
3.  **Study Deck:** Initiates the study mode for the selected deck. Cards are presented, and you can indicate whether you answered correctly to adjust their review frequency.
4.  **Edit Deck:** Provides a submenu with options to edit existing cards, sort the deck, search for cards add new cards, or change the study mode.
5.  **Export Deck:** Allows you to save a copy of the currently selected deck to a location of your choice.
6.  **Import Deck:** Enables you to load a deck from a `.csv` file located elsewhere on your system.
7.  **Exit:** Closes the application.

## Data Storage

Decks are stored as `.csv` files in the `Decks` directory. Each row in the `.csv` file represents a flashcard with the question, answer, creation date, current interval, ease factor, times reviewed, times failded, and times correct separated by commas.

## Class Structure

* **`HashTable`:** A basic hash table implementation used for efficient searching of cards by question within a deck. It uses linear probing for collision resolution and supports insertion, retrieval, and deletion of key-value pairs.
* **`PriorityQueue`:** A priority queue implementation using the `heapq` module. It is used in the `DeckSchedule` to manage the order in which cards are presented for studying based on their review time.
* **`Stack`:** A basic stack implementation used mainly used for the `GraphAdjL` implementation.
* **`Queue`:** A basic queue implementation used mainly used for the `GraphAdjL` implementation.
* **`GraphAdjL`:** A adjacency list graph implementation used for storing cards. It is used in `DeckSchedule` to determine what the next best card to be presented.
* **`Deck`:** The main class for managing flashcard decks. It provides methods for creating, selecting, extracting, importing, exporting, studying, and editing decks.
* **`Card`:** Represents a single flashcard with attributes for the question, answer, creation date, review time,current interval, ease factor, times reviewed, times failded, and times correct.
* **`DeckSchedule`:** Manages the scheduling of cards for studying using a priority queue and graph. It keeps track of when cards should be reviewed next.

## Functions

* **`printCards(deck)`:** Prints the question, answer, and creation date of all cards in a given deck with an index for easy selection.
* **`quickSort(ar, low, high, obj_func)`:** Implements the quicksort algorithm to sort a list of `Card` objects based on a specified attribute (`answer`, `question`, or `date`).
* **`main()`:** The main function that runs the application loop and handles user interactions with the menu.

## Notes

* The maximum number of cards allowed in a single deck is 100.
* Deck names cannot contain the following characters: `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`.
* Imported deck files must have a header row: `question,answer,date_created`.

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for more information
