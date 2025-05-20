import csv, os, shutil, heapq
import random
from datetime import datetime as dt

class Queue:
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        if not self.isEmpty():
            return self.queue.pop(0)

    def peek(self):
        if not self.isEmpty():
            return self.queue[0]

class Stack:
    def __init__(self):
        self.stack = []

    def isEmpty(self):
        return len(self.stack) == 0

    def push(self,data):
        self.stack.append(data)

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()

    def peak(self):
        if not self.isEmpty():
            return self.stack[-1]

class GraphAdjL:  #graph for adj List
    def __init__(self):
        self.graph = {}

    def addVertex(self,data):
        if data not in self.graph:
            self.graph[data] = []

    def addEdge(self,vertex_1,vertex_2): #add w as a paramater for a weighted graph
        if vertex_1 in self.graph and vertex_2 in self.graph:
            if vertex_1 != vertex_2 and vertex_2 not in self.graph[vertex_1]:
                self.graph[vertex_1].append(vertex_2)
                self.graph[vertex_2].append(vertex_1) #remove this line for a directed graph

        else:
            print("One or more edges do not exist")

    def displayGraph(self):
        for vertex,edge in self.graph.items():
            print(f"{vertex}:{edge}")

    def bfs(self,start_vert):
        if start_vert not in self.graph:
            return

        vertices = Queue()
        vertices.enqueue(start_vert)
        visited = set()

        while not vertices.isEmpty():
            current_vert = vertices.dequeue()
            if current_vert not in visited:
                visited.add(current_vert)
                print(current_vert)
            for neighbor in self.graph[current_vert]:
                if neighbor not in visited:
                    vertices.enqueue(neighbor)

    def dfs(self,start_ver):
        if start_ver not in self.graph:
            return

        stack = Stack()
        stack.push(start_ver)
        visited = set()

        while not stack.isEmpty():
            current_vert = stack.pop()
            if current_vert not in visited:
                visited.add(current_vert)
                print(current_vert)
            for n in self.graph[current_vert]:
                 if n not in visited:
                     stack.push(n)

class HashTable:
    def __init__(self,size):
        self.size = size
        self.table = [None] * self.size
        self.deleted = "deleted"

    def hashFunction(self,key):
        return abs(hash(key)) % self.size

    def insert(self,key,card):
        #hash key to find index
        index = self.hashFunction(key)
        count = 0

        #check is hashed index free? if so then we put key,value there
        while count < self.size:
            if self.table[index] is None or self.table[index] == self.deleted or self.table[index][0] == key:
                self.table[index] = (key,card)
                return
            #if not linear probe keep checking the next index for a spot wrap around if nessasary
            index = (index + 1) % self.size
            count += 1

    def get(self,key):
        #hash out initial index
        index = self.hashFunction(key)
        count = 0

        while count < self.size:
            if self.table[index] is None:
                return None
            if self.table[index] != self.deleted and self.table[index][0] == key:
                return self.table[index][0],self.table[index][1]
            index = (index + 1) % self.size
            count += 1
        return None

    def delete(self,key):
        index = self.hashFunction(key)
        count = 0

        while count < self.size:
            if self.table[index] is None:
                return None
            if self.table[index] != self.deleted and self.table[index][0] == key:
                poppedValue = self.table[index]
                self.table[index] = self.deleted
                return poppedValue
            index = (index + 1) % self.size
            count += 1
        return None

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def isEmpty(self):
        return len(self.heap) == 0

    def enqueue(self,priority, data):
        heapq.heappush(self.heap,(priority,data))

    def dequeue(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]

class Deck:
    def __init__(self,path):
        """
        A basic deck class where the user can make decks, select a deck to use, study the selected deck, edit the selected deck,
        export selected deck, and import other decks

        Parameters:
        path (str): A string representing the directory where the decks are stored

        Returns:
        None
        """
        self.path = path
        self.deck = None
        self.deckName = None
        self.study_deck = DeckSchedule(1,"review_time")
        self.hash_table = None
        self.invalidChars = ["\\", "/", ":", "*", "?", '"', "<", ">","|"]  # characters that can not be in a file's name in windows
        self.study_mode = "review_time"
        self.card_threshold = 0.6  #default

    def makeDeck(self):
        """
        Generates a deck based on the users inputs as a csv file

        Parameters:
        None

        Returns:
        None
        """
        deck = []
        deck.append(["question", "answer", "date_created","cur_interval","ease_factor","times_reviewed","times_failed","times_correct"])  # header for the csv
        existingDecks = os.listdir(self.path)
        while True:
            deckName = input("Name of the deck:\n")

            if any(char in deckName for char in self.invalidChars):  # if any invalid characters are in the deck name
                print(f"The name can not contain:")
                print(*self.invalidChars, sep=",")
                print("\n")

            elif deckName == "":
                print("The deck must have a name!")

            elif deckName + '.csv' in existingDecks:  # checks for duplicates
                print("Duplicate deck name try another name!")

            else:
                break

        card = self.makeCard()
        deck.append(card)

        while len(deck) < 101:
            if len(deck) == 101:
                print("You have reached the maximum limit of 100 cards in this deck.")
                break

            choice = input("Do you want to add more cards?\n1): Yes:\n2): No:\n")

            if choice == "2":
                break
            elif choice == "1":
                card = self.makeCard()
                deck.append(card)
            else:
                print("Invalid Input! Please enter '1' for Yes or '2' for No.")

        with open(self.path + "\\" + deckName + ".csv", "w", newline='') as f:
            w = csv.writer(f)
            w.writerows(deck)

    def makeCard(self):
        """
        Generates a card based on the users inputs and adds it to the deck

        Parameters:
        deck (arr): array of all cards to store as a csv

        Returns:
        None
        """
        card = []
        while True:
            question = str(input("Question for the card:\n"))
            if question == "":
                print("The card must have a question!")
            else:
                break
        while True:
            answer = str(input("Answer for the card:\n"))
            if answer == "":
                print("The card must have a answer!")
            else:
                break
        now = str(dt.now().date()) + " " + str(dt.now().time())[:-7]  # gets current date and time
        card.append(question)
        card.append(answer)

        cur_interval = 1
        times_reviewed = 0
        times_failed = 0
        times_correct = 0
        ease_factor = 2.5

        card.append(now)
        card.append(cur_interval)
        card.append(ease_factor)
        card.append(times_reviewed)
        card.append(times_correct)
        card.append(times_failed)

        return card

    def extractDeck(self):
        """
        Extracts all information from the selected deck

        Parameters:
        None:

        Returns:
        deck: (arr): An array where the data from a csv is stored
        """
        try:
            deck = []
            with open(self.path + self.deckName, "r") as text:
                csv = text.readlines()
                csv.pop(0)
                for n, line in enumerate(csv, 1):
                    line = line.replace("\n", "") #get rid of "\n"
                    line = line.split(",")
                    card = Card(line[0], line[1], line[2], n, line[3], float(line[4]), int(line[5]), int(line[6]),int(line[7]))
                    self.study_deck.addCard(card,float(line[4]))
                    deck.append(card)


            self.deck = deck
            self.hash_table = HashTable(101)
            for card in self.deck:
                self.hash_table.insert(card.question.lower(), card)
            return self.deck

        except:
            print("An error occurred")

    def selectDeck(self):
        """
        Returns a string of the decks name that the user chose, if valid

        Parameters:
        None

        Returns:
        str: A string of the deck name the user chose
        """
        existingDecks = os.listdir(self.path)
        if not existingDecks:
            print("There are no decks to select!\nYou can make decks at the main menu")
            return

        else:
            while True:
                print("Select a deck:")
                for idx, d in enumerate(existingDecks, 1):
                    print(f"{idx}): {d[:-4]}")
                deck_choice = input("")
                if deck_choice.isnumeric() and 1 <= int(deck_choice) <= len(existingDecks):
                    selectedDeck = existingDecks[int(deck_choice) - 1]
                    self.deckName = selectedDeck
                    return self.deckName
                else:
                    print("\nEnter a existing deck!")

    def importDeck(self):
        """
        Allows user to import a deck, if valid

        Parameters:
        None

        Returns:
        None
        """
        deckImport = input("Enter the path to the deck you want to import:\n")
        try:
            if not os.path.exists(deckImport):
                print("File not found")
                return

            with open(deckImport, "r") as f:
                text = f.read().strip()
                if text.partition("\n")[0] != "question,answer,date_created,cur_interval,ease_factor,times_reviewed,times_failed,times_correct": #check for header
                    print("Invalid file!")
                    return
                f.close()
                filename = os.path.basename(deckImport)
                destinationPath = os.path.join(self.path, filename)
                shutil.copy(deckImport, destinationPath) #create a copy of the deck
                print("Deck imported successfully")

        except Exception as e:
            print(e)

    def exportDeck(self):
        """
        Allows user to export existing decks, if valid

        Parameters:
        None

        Returns:
        None
        """
        cur_name = self.deckName
        selectedDeck = self.selectDeck()
        self.deckName = cur_name # resets deck name to original one

        try:
            deckExport = input("Enter the path to the deck you want to export to:\n")
            if not os.path.isdir(deckExport):
                print(f"'{deckExport}' is not a valid directory.")
                return

            shutil.copy(self.path + '\\' + selectedDeck, deckExport) #create a copy of the deck
            print("Successful")

        except Exception as e:
            print(e)

    def studyDeck(self):
        """
        A function where the user could study cards from the selected deck. The frequency of cards appearing is based on their review time
        If a custom study mode is active then a custom study mode is selected.

        Parameters:
        None

        Returns:
        None
        """

        if self.study_mode != "review_time":
            self.customStudy()

        else:
            if not self.deck:
                print("You need to select a deck first!")
                return

            deck_copy = self.study_deck

            while not deck_copy.priority_deck.isEmpty():
                card_to_review = deck_copy.getNextCard()
                if card_to_review:
                    print("Question:")
                    print(card_to_review.question)
                    input("\nPress enter to see the answer")
                    print("\nAnswer:")
                    print(card_to_review.answer, "\n")
                    card_to_review.cur_interval = card_to_review.ease_factor*self.study_deck.interval_modify
                    new_interval = card_to_review.cur_interval * card_to_review.ease_factor * self.study_deck.interval_modify

                    while True:
                        choice = input("1): Again, 2): Hard, 3): Good, 4): Easy, 5): Remove Card, or 6): Exit\n")
                        if choice == '1':
                            card_to_review.times_reviewed += 1
                            card_to_review.times_failed += 1
                            deck_copy.removeCard()
                            card_to_review.editCardValues(self.path,self.deckName,card_to_review.ease_factor,card_to_review.ease_factor)
                            deck_copy.updateReviewTime(card_to_review,card_to_review.ease_factor)
                            break

                        elif choice == '2':
                            card_to_review.times_reviewed += 1
                            card_to_review.times_failed += 1
                            deck_copy.removeCard()
                            card_to_review.editCardValues(self.path, self.deckName, card_to_review.ease_factor,card_to_review.cur_interval*self.study_deck.interval_modify*1.2)
                            deck_copy.updateReviewTime(card_to_review,card_to_review.cur_interval*self.study_deck.interval_modify*1.2)
                            break

                        elif choice == '3':
                            card_to_review.times_reviewed += 1
                            card_to_review.times_correct += 1
                            deck_copy.removeCard()
                            card_to_review.editCardValues(self.path, self.deckName, card_to_review.ease_factor,new_interval)
                            deck_copy.updateReviewTime(card_to_review,new_interval)
                            break

                        elif choice == "4":
                            card_to_review.times_reviewed += 1
                            card_to_review.times_correct += 1
                            deck_copy.removeCard()
                            card_to_review.editCardValues(self.path, self.deckName, card_to_review.ease_factor + 1.5,new_interval)
                            deck_copy.updateReviewTime(card_to_review,new_interval)
                            break

                        elif choice == "5":
                            card_to_review.editCardValues(self.path, self.deckName, card_to_review.ease_factor,new_interval)
                            deck_copy.removeCard()
                            break

                        elif choice == "6":
                            return

                        else:
                            print("Invalid Input!")

    def editDeck(self):
        """
        A function where the user can edit specific cards, add cards to the selected deck, sort cards by date
        created, answer, or question, search for a specific card, or change the current study mode.

        Parameters:
        None

        Return:
        None
        """
        if self.deck is None:
            print("You need to select a deck first!")
            return

        while True:
            print(""
                  "1): Edit Cards\n"
                  "2): Sort Cards\n"
                  "3): Search Card\n"
                  "4): Add Card\n"
                  "5): Select Study Mode\n"
                  "6): Back"
                  )
            choice = input("Select an option: ")

            if choice == "6":
                break

            if choice == "1":
                while True:
                    printCards(self.deck)
                    card_index = input("Select a card to edit:")
                    if card_index.isnumeric() and int(card_index) == len(self.deck) + 1:
                        break

                    elif card_index.isnumeric() and 0 <= int(card_index) - 1 < len(self.deck):
                        card_index = int(card_index) - 1
                        card = self.deck[card_index] #get the selected card

                        #removes from hash table and add the new one
                        self.hash_table.delete(card.question.lower())
                        card.askCard(self.path, self.deckName)
                        self.hash_table.insert(card.question.lower(), card)
                    else:
                        print("Invalid input!")

            elif choice == "2":
                while True:
                    print("Sort by what?"
                          "\n1): Answer alphabetically"
                          "\n2): Question alphabetically"
                          "\n3): Last Created"
                          "\n4): Back"
                          )
                    edit = input("Select an option:")
                    if edit == "4":
                        break
                    #sorts based on input
                    elif edit == "1":
                        self.deck = quickSort(self.deck, 0, len(self.deck) - 1, "answer")
                        print("Deck sorted by answer.")
                        break
                    elif edit == "2":
                        self.deck = quickSort(self.deck, 0, len(self.deck) - 1, "question")
                        print("Deck sorted by question.")
                        break
                    elif edit == "3":
                        self.deck = quickSort(self.deck, 0, len(self.deck) - 1, "date")
                        print("Deck sorted by date.")
                        break
                    else:
                        print("Invalid Input!")

            elif choice == "3":
                while True:
                    print("Search by what?"
                          "\n1): Question"
                          "\n2): Back"
                          )
                    edit = input("Select an option:")
                    if edit == "2":
                        break  # break from loop


                    elif edit == "1":
                        question = input("Enter question to search for:")
                        found_card = self.hash_table.get(question.lower())
                        if found_card:
                            card = found_card[1]
                            while True:
                                print(f"\nFound, edit the card?"
                                      f"Card): Question):{card.question} Answer): {card.answer} Date Created): {card.date}"
                                      "\n1): Yes"
                                      "\n2): No")
                                search_card_edit = input("Select an option:")
                                if search_card_edit == "1":
                                    #removes from hash table and add the new one
                                    self.hash_table.delete(card.question.lower())
                                    card.editCard(self.path, self.deckName)
                                    self.hash_table.insert(card.question.lower(),card)
                                elif search_card_edit == "2":
                                    break
                                else:
                                    print("Invalid Input!")
                        else:
                            print("Card not found")

                    else:
                        print("Invalid Input!")

            elif choice == "4":
                if len(self.deck) > 101:
                    print("You reached the max amount of cards in a deck.\nA deck cannot have more than 100 cards!")
                    return
                card_list = self.makeCard()
                card = Card(card_list[0], card_list[1], card_list[2], len(self.deck)+1, card_list[3], float(card_list[4]), int(card_list[5]), int(card_list[6]),int(card_list[7]))

                #adds it to all decks
                self.deck.append(card)
                self.study_deck.addCard(card)
                self.hash_table.insert(card.question.lower(),card)
                with open(self.path + "\\" + self.deckName, "a", newline='') as f:
                    w = csv.writer(f)
                    w.writerow(card_list)
                print("Card added")

            elif choice == "5":
                self.setStudyMode()
                print("\n")

            else:
                print("Invalid input!")

    def setStudyMode(self):
        """
        A function where the user can set the study mode based on hard or easy cards.

        Parameters:
        None

        Return:
        None
        """
        while True:
            print("\nSelect Study Mode:")
            print("1): Review Schedule")
            print("2): Review Hard Cards")
            print("3): Review Easy Cards")
            print("4): Back")
            mode_choice = input("Enter your choice: ")
            #changes stduy_mode based on user inputs
            if mode_choice == "1":
                self.study_mode = "review_time"
                print(f"Studying on review time")
                break
            elif mode_choice == "2":
                self.study_mode = "study_hard"
                print(f"Studying hard cards")
                print(self.study_mode)
                break
            elif mode_choice == "3":
                self.study_mode = "study_easy"
                print(f"Studying easy cards")
                break
            elif mode_choice == "4":
                break
            else:
                print("Invalid choice.")

    def customStudy(self):
        """
        A function where the user could study cards from the selected deck. The cards appearing will be based on card_threshold.

        Parameters:
        None

        Returns:
        None
        """
        if not self.deck:
            print("You need to select a deck first!")
            return

        #Create data structures
        study_graph = GraphAdjL()
        deck = DeckSchedule(1,self.study_mode)

        #populate data structures if a cards meets a threshold
        for card in self.deck:
            card_study_value = getattr(card, self.study_mode)
            if card_study_value >= self.card_threshold:  # will apply to both easy and hard
                deck.addCard(card,card_study_value*-1)
                study_graph.addVertex(card)

        #add edges to between all cards
        temp = list(study_graph.graph.keys())
        for i in range(len(temp)):
            for n in range(i + 1, len(temp)):
                study_graph.addEdge(temp[i], temp[n])

        visited = set()
        card_to_review = None

        while not deck.priority_deck.isEmpty():
            card_to_review = deck.getNextCard(self.study_mode,card_to_review,study_graph,visited)
            if card_to_review:
                print("Question:")
                print(card_to_review.question)
                input("\nPress enter to see the answer")
                print("\nAnswer:")
                print(card_to_review.answer, "\n")

                while True:
                    choice = input("1): Again, 2): Hard, 3): Good, 4): Easy, 5): Remove Card, or 6): Exit")

                    if choice == '1':
                        card_to_review.times_failed += 1
                        card_to_review.times_reviewed += 1
                        break

                    elif choice == '2':
                        card_to_review.times_failed += 1
                        card_to_review.times_reviewed += 1
                        break

                    elif choice == '3':
                        card_study_value = getattr(card_to_review, self.study_mode)
                        card_to_review.times_correct += 1
                        card_to_review.times_reviewed += 1
                        if card_study_value < self.card_threshold:
                            deck.removeCard()
                            visited.add(card_to_review.question)
                            break
                        deck.removeCard()
                        deck.updateReviewTime(card_to_review,card_study_value*-1)

                        break

                    elif choice == "4":
                        card_study_value = getattr(card_to_review, self.study_mode)
                        card_to_review.times_correct += 1
                        card_to_review.times_reviewed += 1
                        if card_study_value < self.card_threshold:
                            deck.removeCard()
                            visited.add(card_to_review.question)
                            break
                        deck.removeCard()
                        deck.updateReviewTime(card_to_review,card_study_value*-1)
                        break

                    elif choice == "5":
                        deck.removeCard()
                        visited.add(card_to_review.question)
                        break

                    elif choice == "6":
                        return

                    else:
                        print("Invalid Input!")

class Card:
    def __init__(self,question,answer,date,row_number,cur_interval,ease_factor,times_reviewed,times_failed,times_correct):
        """
        A basic card class that makes each card in a deck a card

        Parameters:
        question (str): The question to a card
        answer (str): The answer to a card
        date (str): The date the cards was created on
        row_number (int): A number that shows which row a card is stored in the csv
        cur_interval (int): The interval of the card
        ease_factor (float): The ease factor of the card
        times_reviewed (int): The total times the card has been reviewed
        times_failed (int): Total times the card has been failed
        times_correct (int): Total times the card has been answered correctly

        Returns:
        str: The question of a card
        stt: Thr answer of a card
        str: The date the cards was created on
        """

        self.question = question
        self.answer = answer
        self.date = date
        self.row = row_number
        self.review_time = 1 #default review time
        self.cur_interval = cur_interval
        self.ease_factor = ease_factor #2.5 default
        self.times_reviewed = times_reviewed
        self.times_failed = times_failed
        self.times_correct = times_correct

    @property
    def study_hard(self):
        """
        Calculates the hardness of a card.

        Parameters:
        None

        Returns:
        float: A value representing the card's hardness
        """

        return (self.times_failed+1) / (self.times_reviewed + 1)

    @property
    def study_easy(self):
        """
        Calculates the easiness of a card.

        Parameters:
        None

        Returns:
        float: A value representing the card's easiness
        """

        return (self.times_correct+1) / (self.times_reviewed + 1)

    def __lt__(self, other):
        """
        Determines if a card is less the another one

        Parameters:
        other (Card): A card class to compare with

        Return
        bool: True if card's review_timme is less than the other card's review_time, and False otherwise
        """

        return self.review_time < other.review_time

    def displayQuestion(self):
        return self.question

    def displayAnswer(self):
        return self.answer

    def displayDateCreated(self):
        return self.date

    def askCard(self,path,deckName):
        """
        A function that prints a menu where the user can edit a card or exit the menu

        Parameters:
        path (str): A string representing the directory where the decks are stored
        deckName (str): The name of the selected deck

        Returns:
        None
        """
        while True:
            print(
                f"Question): {self.question} Answer):{self.answer} Date Created): {self.date}")
            print(""
                  "1): Edit Question/Answer\n"
                  "2): Back"
                  )
            edit = input("Select an option:")
            if edit == "2":
                break  # break go back
            elif edit == "1":  # edits question
                self.editCard(path,deckName)
                print("Card successfully edited")
            else:
                print("Invalid input!")

    def editCard(self,path,deckName):
        """
        A function where the user can edit a cards question or answer

        Parameters:
        path (str): A string representing the directory where the decks are stored
        deckName (str): The name of the selected deck

        Return:
        None
        """
        with open(path + "\\" + deckName, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)  # store rows for editing
        while True:
            print("Old Question:")
            print(self.question)
            choice = input("1): Edit Question"
                           "\n2): Skip")
            if choice == "1":
                newQuestion = input("\nWhat is the new question:\n")
                rows[self.row][0] = newQuestion
                with open(path + "\\" + deckName, "w", newline='') as f:
                    w = csv.writer(f)
                    w.writerows(rows) # write new question
                    self.question = newQuestion
                    break

            elif choice == "2":
                break

            else:
                print("Invalid Input!")
        while True:
            print("Old Answer:")
            print(self.answer)
            choice = input("1): Edit Answer"
                           "\n2): Skip")
            if choice == "1":
                newAnswer = input("\nWhat is the new answer:\n")
                rows[self.row][1] = newAnswer
                with open(path + "\\" + deckName, "w", newline='') as f:
                    w = csv.writer(f)
                    w.writerows(rows)# write new answer
                    self.answer = newAnswer
                    break
            elif choice == "2":
                break

            else:
                print("Invalid Input!")

    def editCardValues(self, path,deck_name, ease, cur_interval):
        """
        Updates the card's review values in the deck's CSV file.

        Parameters:
        path (str): The directory where the deck is located
        deck_name (str): The name of the deck's CSV file
        ease (float): The new ease factor for the card
        cur_interval (float): The new interval for the card

        Returns:
        None
        """

        with open(os.path.join(path, deck_name), "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)  # store rows for editing
            rows[self.row][3] = cur_interval
            rows[self.row][4] = ease
            rows[self.row][5] = self.times_reviewed
            rows[self.row][6] = self.times_failed
            rows[self.row][7] = self.times_correct

        with open(os.path.join(path,deck_name), "w", newline='') as f:
            w = csv.writer(f)
            w.writerows(rows)

class DeckSchedule:
    def __init__(self,interval_modify,study_type):
        """
        Initializes a deck to be studied as a Priority Queue

        Parameters:
        interval_modify (int): The interval for the deck
        study_type (str): The current study mode

        Returns:
        None
        """
        self.priority_deck = PriorityQueue()
        self.interval_modify = interval_modify
        self.study_type = study_type

    def addCard(self,card,priority=2.5):
        """
        Adds a card with a priority number and their info to the priority queue

        Parameters:
        card (Card): The card to be added to the priority queue
        priority (float): The new priority of the card. (Defaults to 2.5)

        Returns:
        None
        """
        self.priority_deck.enqueue(priority,card)

    def removeCard(self):
        """
        Removes a card if it is over review date

        Parameters:
        None

        Returns:
        None
        """
        return self.priority_deck.dequeue()

    def updateReviewTime(self,card,priority):
        """
        Updates a card review time based on if the user knows/does not know the card for more frequent review

        Parameters:
        card (Card): The card to edit
        priority (int): The time to change in the review time

        Returns:
        None
        """
        self.addCard(card,priority)

    def getNextCard(self,atrb=None,cur_card=None,graph=None,visited=None):
        """
        A function that returns the next best card based on the study_mode.

        Parameters:
        atrb (str): The study_mode variable that determines what the next best card is
        cur_card (Card): The current card that is being studied
        graph (GraphAdjl): A graph that shows the relationships between cards
        visited (set): A set containing cards that are already visited

        Returns:
        Card or None: The next card to be studied or None if there is no card found
        """

        next_card = None
        if cur_card:
            if self.study_type != "review_time":
                cur_highest = 0
                for neighbor in graph.graph[cur_card]:
                    if neighbor.question not in visited:
                        if getattr(neighbor,atrb) > cur_highest:
                            cur_highest = getattr(neighbor,atrb)
                            next_card = neighbor
                        if getattr(cur_card,atrb) > getattr(next_card,atrb) and cur_card not in visited:
                            return cur_card
                        else:
                            return
                return next_card

        else:
            return self.priority_deck.heap[0][1]

directory = os.path.join(".", "Decks") + os.sep # replace with any desired path to store the decks

def printCards(deck):
    """
    Print all the cards information in a deck

    Parameters
    deck (arr): An array containing all cards in the deck

    Returns
    None
    """
    for n, card in enumerate(deck, 1):
        print(f"{n}): Question): {card.question} Answer):{card.answer} Date Created): {card.date}")
    print(f"{len(deck) + 1}): Back")

def quickSort(ar, low, high, obj_func):
    if low >= high:
        return

    pivot_index = random.randint(low, high)
    ar[pivot_index], ar[high] = ar[high], ar[pivot_index]
    pivot = getattr(ar[high], obj_func)

    i = low - 1
    for j in range(low, high):
        if getattr(ar[j], obj_func) < pivot:
            i += 1
            ar[i], ar[j] = ar[j], ar[i]

    ar[i + 1], ar[high] = ar[high], ar[i + 1]
    partition_index = i + 1

    quickSort(ar, low, partition_index - 1, obj_func)
    quickSort(ar, partition_index + 1, high, obj_func)

    return ar

deck = Deck(directory)

def main():
    while True:
        print("\n"*2)
        print(""
              "1): Make Deck"
              "\n2): Select Deck"
              "\n3): Study Deck"
              "\n4): Edit Deck"
              "\n5): Export Deck"
              "\n6): Import Deck"
              "\n7): Exit"
              )
        menuChoice = input("Choose an option:\n")

        if menuChoice == "7":
            break
        elif menuChoice == "1":
            deck.makeDeck()
        elif menuChoice == "2":
            deck.selectDeck()
            deck.extractDeck()
        elif menuChoice == "3":
            deck.studyDeck()
        elif menuChoice == "4":
            deck.editDeck()
        elif menuChoice == "5":
            deck.exportDeck()
        elif menuChoice == "6":
            deck.importDeck()
        else:
            print("Invalid Input!")

if __name__ == "__main__":
    main()