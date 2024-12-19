import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QMainWindow, QSplitter
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtCore import Qt, QSize


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development and PyInstaller.
    :param relative_path: Relative file path to the resource
    :return: Absolute file path
    """
    # Adjust for images directory
    relative_path = os.path.join("images", relative_path)

    if hasattr(sys, '_MEIPASS'):  # When bundled with PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)


class AdventureGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window size to 50% of the screen
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.6)
        height = int(screen.height() * 0.6)
        self.resize(width, height)

        self.setWindowTitle('Creepy Monk')
        self.start_screen()

        self.location_full_names = {
            'purgatory': 'Purgatory',
            'elvira': 'Elvira\'s Apartment',
            'matilda': 'Matilda in the Monastery',
            'antonia': 'Antonia\'s Tomb'
        }
        self.end_paragraphs = [
            "Ambrosio blinked as the air around him grew still and heavy, the suffocating weight of judgment returning. The faint glow of divine light "
            "illuminated the vast, ethereal space, and before him stood the canvas—blank, waiting, and unrelenting.<br>",

            "God: Your journey is complete, Ambrosio. Now, face the truth of your sins. Take the brush, and let your hand reveal what lies within your soul.<br>",

            "The painting hovered before him, incomplete but alive with swirling colors—black for death, red for violence, white for innocence, gold for ambition, "
            "sable for deceit, and rose for faith betrayed. Ambrosio stood trembling, the brush in his hand as his voice broke the silence.<br>",

            "\"I see it now. The power I held was never mine to take. Elvira, Matilda, Antonia—they trusted me, and I betrayed them. I should have been their protector, "
            "their guide, but I destroyed their faith, their love, and their innocence. This painting is my soul laid bare—my punishment and my confession. Let it stand not "
            "only for my sins but as a warning to all who would misuse power. I see my pride, my cruelty, my sin. For that, I repent, and for that, I accept judgment.\"<br>",

            "With trembling hands, Ambrosio raised the brush and made the final stroke. The swirling colors stilled, and the image emerged: a towering man shrouded in shadow, "
            "holding a limp, veiled woman. Her sorrowful figure seemed alive, her delicate frame a silent accusation, while his looming presence radiated guilt and unrelenting power.<br>",

            "The painting pulsed with light, sharp and piercing, its glow illuminating the void. Slowly, Ambrosio reached for the brush one last time and signed his name at the bottom "
            "of the canvas. As the final mark dried, the canvas began to rise, hovering in the air.<br>",

            "Ambrosio fell to his knees, bowing his head before the painting. His voice, low but resolute, filled the space:<br>",

            "\"I will write a sonnet—a warning to any who see this work, a testament to the ruin pride and power can bring. Let my words and this painting speak together, so no soul "
            "walks the path I have tread.\"<br>",

            "The painting glowed faintly, its light softening, as though awaiting its companion words.<br>",

            "Ambrosio gazed upon the painting, his voice low and heavy with remorse:<br>",

            "\"Men and monks alike wield great power over women, a power that shapes their lives in ways we often fail to see. Their well-being, their dignity, so often rests in our hands, "
            "and it is our choice to either uplift them with grace or crush them with control. As in a dance, men and women are partners in life, moving together in balance and trust. One leads, "
            "the other follows, but neither can thrive without the other.<br>",

            "To hold such power is not a privilege but a sacred responsibility, a duty to protect, to guide with care. Yet I—driven by pride, blinded by lust—turned trust into chains and harmony "
            "into ruin. This painting speaks not only of grace but of the fragility of control. Let it remind all who see it that life itself is a dance, and power, when wielded with cruelty, "
            "destroys not only the one held but also the one who holds. Let us learn to carry others gently, lest we fall together into darkness.\"<br>"
        ]
        self.intro_paragraphs = [
            "'What?' He cried, darting at him a look of fury: 'Dare you still implore the Eternal's mercy? Would you feign penitence, and again "
            "act an Hypocrite's part? Villain, resign your hopes of pardon. Thus I secure my prey!'",

            "As He said this, darting his talons into the Monk's shaven crown, He sprang with him from the rock. The Caves and mountains rang "
            "with Ambrosio's shrieks. The Daemon continued to soar aloft, till reaching a dreadful height, He released the sufferer. Headlong "
            "fell the Monk through the airy waste; The sharp point of a rock received him; and He rolled from precipice to precipice, till bruised "
            "and mangled He rested on the river's banks.",

            "Life still existed in his miserable frame: He attempted in vain to raise himself; His broken and dislocated limbs refused to perform "
            "their office, nor was He able to quit the spot where He had first fallen. The Sun now rose above the horizon; Its scorching beams darted "
            "full upon the head of the expiring Sinner. Myriads of insects were called forth by the warmth; They drank the blood which trickled from "
            "Ambrosio's wounds; He had no power to drive them from him, and they fastened upon his sores, darted their stings into his body, covered him "
            "with their multitudes, and inflicted on him tortures the most exquisite and insupportable. The Eagles of the rock tore his flesh piecemeal, "
            "and dug out his eyeballs with their crooked beaks.",

            "A burning thirst tormented him; He heard the river's murmur as it rolled beside him, but strove in vain to drag himself towards the sound. "
            "Blind, maimed, helpless, and despairing, venting his rage in blasphemy and curses, execrating his existence, yet dreading the arrival of death "
            "destined to yield him up to greater torments, six miserable days did the Villain languish.",

            "On the Seventh a violent storm arose: The winds in fury rent up rocks and forests: The sky was now black with clouds, now sheeted with fire: "
            "The rain fell in torrents; It swelled the stream; The waves overflowed their banks; They reached the spot where Ambrosio lay, and when they "
            "abated carried with them into the river the Corse of the despairing Monk.",

            "- The above was text from Matthew Lewis', <i>The Monk</i>",

            "Darkness swallows Ambrosio as he writhes upon jagged stones that dig mercilessly into his flesh. The suffocating stench of sulfur fills the air, "
            "acrid and choking, mingling with the ceaseless wails of despair that echo like an endless dirge. The oppressive heat scorches his skin, yet offers no light, "
            "leaving him blind to the desolation around him. The faint taste of ash clings to his tongue, dry and bitter.<br>",

            "Then, through the unyielding blackness, a light begins to grow—a sharp, otherworldly brilliance that cuts through the dark. It illuminates nothing yet feels alive, "
            "its clarity piercing yet cool, unlike the searing flames of Hell. Ambrosio shields his eyes with trembling hands. A voice follows, deep and resonant, steady as the toll "
            "of a cathedral bell. It fills the air, at once calming and unrelenting.<br>",

            "\"Ambrosio, my lost and wayward child, you are now in purgatory.\"<br>",

            "The monk trembled, recognizing divinity. His hands, instruments of sin and ambition, now reached toward the light. “Who speaks?” he croaked, his voice hoarse. "
            "“Who dares disturb my torment?”<br>",

            "<b>God:</b> I am the Shepherd who tends even to His stray sheep. I am He whom you once served in purity, before pride led you astray.<br>",

            "Ambrosio fell to his knees. “Lord, why do You now appear, only to witness my torment?”<br>",

            "The light warmed, casting a golden glow.<br>",

            "<b>God:</b> Even in your vilest acts, I did not forget you. I am merciful and offer you a chance to repent.<br>",

            "Ambrosio’s voice faltered. “Repent? After all I have done? My crimes—”<br>",

            "<b>God:</b> Your sins are grievous, Ambrosio, but my mercy is unmeasured. You wronged those placed under your care, defiled innocence, and made others tools of your desires. "
            "Do you understand the depth of your trespass?<br>",

            "Ambrosio bowed his head. “I do, my Lord. Their faces haunt me. Their suffering brands my very soul.”<br>",

            "<b>God:</b> Then hear My will. You will return to the mortal realm—not to live, but to confront the truth of your actions. You will revisit the women you wronged. Through their stories, "
            "you will create a painting—as a testament of your sins. This painting will serve as a warning to other men tempted by Lucifer. It will stand as a reminder of the cost of sin, "
            "and the destruction wrought by turning from My path. Completing this painting will be your task to enter purgatory. Should you fail, you will return here to burn for eternity.<br>",

            "Ambrosio shuddered, the weight of the task pressing upon him. “How can I face them, my Lord? How can I bear their judgment? Those wretched insensible women!”<br>",

            "<b>God:</b> You will see them as they were, as you made them. The truth will guide your hand to paint a work that captures not only their suffering, but your role in their fall.<br>",

            "The light began to fade. Before it vanished, the voice spoke one final time:<br>",

            "<b>God:</b> Ambrosio, will you face your sins and repent to stay in purgatory for the rest of your life?<br>",

            "The monk trembled, then bowed his head.<br>",

            "\"Yes.\"<br>"
        ]


        self.game_state = 'start'  # Start in the 'start' phase
        self.workbench_step = 0  # Initialize the workbench step counter
        self.used_items = []
        self.on_complete = None  # Initialize on_complete callback
        
    def start_screen(self):
        # Create the start button screen
        self.start_widget = QWidget()
        self.setCentralWidget(self.start_widget)
        
        start_layout = QVBoxLayout()
        start_layout.setAlignment(Qt.AlignCenter)
        
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        
        start_layout.addWidget(self.start_button)
        self.start_widget.setLayout(start_layout)
    
    def start_game(self):
        # Set up the main game screen
        self.play_widget = QWidget()
        self.setCentralWidget(self.play_widget)

        # Initialize inventory and ungrabbed items
        self.inventory = []  # Start with an empty inventory
        self.inventory.append(("potion", get_resource_path("map.pdf")))

        # Map locations to available items and their associated images
        self.location_items = {
            'purgatory': {},
            'elvira': {'black': get_resource_path('pigweed.pdf')},
            'antonia': {'red': get_resource_path('moss.pdf'), 'white': get_resource_path('bachelorsbuttons.pdf')},
            'matilda': {'sable': get_resource_path('wildgrapevine.pdf'), 'gold': get_resource_path('Sonnets.pdf'), 'rose': get_resource_path('Sonnets.pdf')}
        }

        # Initialize locations
        self.locations = ['purgatory', 'elvira', 'matilda', 'antonia']
        self.current_location = 'purgatory'  # Starting location

        # Create a splitter to dynamically resize top and bottom sections
        self.splitter = QSplitter(Qt.Vertical)

        # Output area (80% of height)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #CDEBC5; color: black; padding-left: 10px; padding-right: 5px;")
        self.output_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove vertical scrollbar
        self.output_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove horizontal scrollbar
        self.splitter.addWidget(self.output_area)

        # Input area (20% of height)
        self.input_line = QLineEdit()
        self.input_line.setMaxLength(30)
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.setStyleSheet("background-color: lightgrey; color: black; padding-left: 10px;")
        self.input_line.returnPressed.connect(self.process_input)
        self.splitter.addWidget(self.input_line)

        # Adjust the initial splitter ratio
        self.splitter.setSizes([int(self.height() * 0.8), int(self.height() * 0.2)])

        # Set layout with splitter
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.play_widget.setLayout(layout)

        # Start the click-through sequence for the introduction
        self.click_through_text(self.intro_paragraphs, next_state='main', on_complete=self.start_main_game)

    def update_output(self, text, image_path=None):
        self.output_area.moveCursor(QTextCursor.End)
        if image_path:
            self.output_area.insertHtml(f'<img src="{image_path}" width="300"><br>')
        else:
            self.output_area.insertHtml(f'{text}<br>')
        self.output_area.moveCursor(QTextCursor.End)

    def process_input(self):
        user_input = self.input_line.text().strip().lower()
        self.input_line.clear()

        if not user_input:
            return

        # Display the user input in grey
        if user_input:  # Only display if input is not empty
            self.update_output(f"<span style='color:gray;'>{user_input}</span><br>")

        # If in main game state, process the main game commands
        if self.game_state == 'main':
            # Split command into parts, handle multiple spaces
            parts = user_input.split()
            command = parts[0].lower() if parts else ""

            # Validate the command
            valid_commands = ['show', 'list', 'grab', 'help', 'move', 'current', 'use']
            if command not in valid_commands:
                self.update_output(f'<span style="color:black;">{command} is not a valid command.</span><br>')
                return
            
            if self.current_location == 'purgatory':
                # Check for 'use workbench' command
                if command == 'use' and len(parts) > 1 and parts[1].lower() == 'easel':
                    if len([item for item in self.inventory if item[0] not in ['empty canvas']]) < 6:
                        self.update_output("It seems like you do not have enough colours to paint.<br>")
                    else:
                        self.game_state = 'workbench'
                        self.workbench_step = 1  # Start the first step
                        self.update_output("As you stand at the workbench, the equipment glints under the dim light, ready to begin the process that might undo the garden’s cruelty. "
                                           "The recipe's first step is clear: to add the liquid base into the titrant.<br>"
                                           "<br>The base must be selected carefully. What will you add?<br>")
                        self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it.<br>")
                        self.list_inventory()
                    return
                elif command == 'use':
                    self.update_output("Invalid syntax. Use '<b>use workbench</b>' to interact with the workbench in the Lab.<br>")
                    return

            if command == 'use' and len(parts) > 1 and parts[1].lower() == 'potion':
                if self.current_location == 'purgatory':
                    self.click_through_text(
                        self.end_paragraphs,
                        next_state='ended',
                        on_complete=self.end_game_message
                    )
                else:
                    self.update_output("The potion is meant for Beatrice's body. Move to her location first.<br>")

            # Handle 'help' command
            if command == 'help':
                if self.game_state == 'workbench':
                    self.update_output("You are using the workbench to create a potion. Follow the prompts to select items from your inventory.<br>")
                    return

                self.update_output('Welcome to Creepy Monk!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to elvira\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: <b>\'purgatory\'</b> for Purgatory, <b>\'elvira\'</b> for Elvira\'s Apartment,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>\'matilda\'</b> Matilda in the Monestary, and <b>\'antonia\'</b> for Antonia\'s Tomb<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'grab\' followed by a reachable colour to grab the colour and add it to your inventory  (note, items are bolded)<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory, and all colours available to grab<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
                return

            # Handle 'current location' command
            if command == 'current' and len(parts) > 1 and parts[1].lower() == 'location':
                full_location_name = self.location_full_names.get(self.current_location, self.current_location)
                self.update_output(f"You are currently at {full_location_name}.<br>")
                return
            elif command == 'current':
                self.update_output("Invalid syntax. Use 'current location'.<br>")
                return

            # Handle 'grab' command
            if command == 'grab':
                item_name = " ".join(parts[1:])  # Combine the rest into the item name
                available_items = self.location_items.get(self.current_location, {})
                if item_name in available_items:
                    # Safely retrieve the file name
                    image_file = available_items[item_name]
                    # Add item to inventory and remove from location
                    self.inventory.append((item_name, image_file))
                    del self.location_items[self.current_location][item_name]
                    self.update_output(f"You grabbed {item_name}.<br>")
                    self.show_pdf(image_file)  # Automatically display the item after grabbing
                elif any(i[0] == item_name for i in self.inventory):
                    self.update_output(f"{item_name} is already in your inventory!<br>")
                else:
                    self.update_output(f"There is no colour '{item_name}' to grab at this location.<br>")
                return

            # Handle 'list items' command
            if command == 'list':
                if len(parts) == 2 and parts[1] == 'items':
                    if self.inventory:
                        inventory_items = ', '.join(item[0] for item in self.inventory)
                        self.update_output(f"Items in your inventory: {inventory_items}<br>")
                    else:
                        self.update_output("Your inventory is empty.<br>")
                    location_items = self.location_items.get(self.current_location, {})
                    if location_items:
                        location_items_list = ', '.join(location_items.keys())
                        self.update_output(f"Items available at this location: {location_items_list}<br>")
                    else:
                        self.update_output("No items available to grab at this location.<br>")
                    return
                else:
                    self.update_output(f"'list' is not a valid command. Did you mean 'list items'?<br>")
                return

            # Handle 'show' command
            if command == 'show':
                item_name = " ".join(parts[1:])  # Combine the rest into the item name
                for inv_item, image_file in self.inventory:
                    if inv_item == item_name:
                        self.update_output(f"Showing {item_name}.<br>")
                        self.show_pdf(image_file)
                        return
                self.update_output(f"You do not have '{item_name}' in your inventory.<br>")
                return

            # Handle 'move to' command
            if command == 'move' and len(parts) > 1 and parts[1].lower() == 'to':
                location = " ".join(parts[2:])  # Combine remaining parts into the location name
                if location in self.locations:
                    if location == self.current_location:
                        self.update_output(f"You are already at {location}!<br>")
                    else:
                        self.enter_area(location)
                else:
                    self.update_output(f"{location} is not a valid location.<br>")
                return
            elif command == 'move':
                self.update_output(f"Invalid syntax. Use 'move to {location}'.<br>")
                return
            
        if self.game_state == 'workbench':

            if user_input.lower() == 'list items':
                self.list_inventory()
                return

            if user_input.lower().startswith('show '):
                item_name = user_input[5:].strip()  # Extract the item name after 'show '
                for item, file_name in self.inventory:
                    if item.lower() == item_name.lower():
                        self.update_output(f"<span style='color:black;'>Showing {item}.</span><br>")
                        self.show_pdf(file_name)
                        return
                self.update_output(f"<span style='color:black;'>You do not have {item_name} in your inventory.</span><br>")
                return

            if self.workbench_step == 1:
                base = user_input.strip()
                if any(item[0] == base and base not in self.used_items and item[0] not in ['potion', 'sonnets', 'map'] for item in self.inventory):
                    self.selected_base = base
                    self.used_items.append(base)  # Mark base as used
                    self.update_output(f"You selected {base} as the base.<br>")
                    self.workbench_step = 2
                    self.update_output("The beaker sits above the flickering Bunsen burner, its glass shimmering faintly in the firelight. "
                                    "This is the critical moment—the base is ready, but the potion requires the precise addition of ingredients to transform it into the antidote. "
                                    "You must carefully add three special components, followed by three specific plants gathered from the garden.<br>"
                                    "Precision is everything. The wrong ingredient will ruin the mixture, and failure comes at a cost. Focus, recall what you’ve learned, and proceed with care.<br>"
                                    "Please enter the first ingredient:<br>")
                    self.list_inventory()  # Show available items
                else:
                    self.update_output(f"{base} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show sonnets\'<br>")
                return

            if self.workbench_step == 2:
                ingredient1 = user_input.strip()
                if any(item[0] == ingredient1 and ingredient1 not in self.used_items and item[0] not in ['potion', 'sonnets', 'map'] for item in self.inventory):
                    self.selected_ingredient1 = ingredient1
                    self.used_items.append(ingredient1)  # Mark ingredient as used
                    self.update_output(f"You added {ingredient1} to the potion.<br>")
                    self.workbench_step = 3
                    self.update_output("Please enter the second ingredient:<br>")
                    self.list_inventory()  # Show available items
                else:
                    self.update_output(f"{ingredient1} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show sonnets\'<br>")
                return

            if self.workbench_step == 3:
                ingredient2 = user_input.strip()
                if any(item[0] == ingredient2 and ingredient2 not in self.used_items and item[0] not in ['potion', 'sonnets', 'map'] for item in self.inventory):
                    self.selected_ingredient2 = ingredient2
                    self.used_items.append(ingredient2)  # Mark ingredient as used
                    self.update_output(f"You added {ingredient2} to the potion.<br>")
                    self.workbench_step = 4
                    self.update_output("Please enter the third ingredient:<br>")
                    self.list_inventory()  # Show available items
                else:
                    self.update_output(f"{ingredient2} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show sonnets\'<br>")
                return

            if self.workbench_step == 4:
                ingredient3 = user_input.strip()
                if any(item[0] == ingredient3 and ingredient3 not in self.used_items and item[0] not in ['potion', 'sonnets', 'map'] for item in self.inventory):
                    self.selected_ingredient3 = ingredient3
                    self.used_items.append(ingredient3)  # Mark the ingredient as used

                    # Check if the recipe is correct
                    correct_base = "green tears"
                    correct_ingredients = {"anemones", "pigweed", "moss"}

                    # Verify the base and the selected ingredients
                    if (self.selected_base == correct_base and
                        {self.selected_ingredient1, self.selected_ingredient2, self.selected_ingredient3} == correct_ingredients):
                        # Success case
                        self.update_output("The potion is ready, its surface glowing faintly as though alive with hope—or perhaps something far more perilous. "
                                        "In your hands lies the culmination of your efforts, the chance to undo the poison that claimed Beatrice’s life.<br>")
                        self.inventory.append(("potion", get_resource_path("potion.pdf")))  # Add potion to inventory
                        self.show_pdf("potion.pdf")  # Open the potion PDF
                        self.update_output("You can now try using the potion on Beatrice's body. Please move to Beatrice's body.<br>")
                    else:
                        # Failure case
                        self.update_output("The beaker begins to bubble uncontrollably, steam rising in angry hisses as the mixture turns an ominous, murky color. "
                                        "Suddenly, with a deafening POP, the concoction explodes upward, splattering scalding liquid and noxious fumes into the air.<br>")
                        self.update_output("Try again using different ingredients, or go out and search for more.<br>")
                        self.update_output("You can try again by typing '<b>use workbench</b>', or go to a different location using a 'move to' command.<br>")

                    # Reset workbench state after the attempt
                    self.used_items = []  # Reset used items for the next session
                    self.workbench_step = 0  # Reset step counter
                    self.game_state = 'main'  # Return to the main game state
                else:
                    self.update_output(f"{ingredient3} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show Sonnets\'<br>")
                return

    def list_inventory(self):
        available_items = [item[0] for item in self.inventory if item[0] not in self.used_items and item[0] not in ['potion', 'sonnets', 'map']]
        if available_items:
            inventory_items = ', '.join(available_items)
            self.update_output(f"Your available inventory: {inventory_items}<br>")
        else:
            self.update_output("No items are currently available for selection.<br>")

    def enter_area(self, location):
        self.current_location = location

        if location == 'purgatory':
            full_location = 'Purgatory'
        elif location == 'elvira':
            full_location = 'Elvira\'s Apartment'
        elif location == 'matilda':
            full_location = 'Matilda in the Monestary'
        elif location == 'antonia':
            full_location = 'Antonia\'s Tomb'

        self.update_output(f"You have arrived at {full_location}.<br>")

        if location == 'purgatory':
            self.click_through_text([
            "The air was heavy and still, smothering all light. Beneath your feet lay soft, green grass, vibrant yet incongruous in the suffocating gloom. Beyond it, nothing remained—only "
            "endless darkness stretching into the void. A thick mist wrapped the world, cloaking everything. A single beam of pale light broke through, casting long, jagged shadows around "
            "you.The silence pressed heavily, a suffocating weight broken now and then by faint, ghostly murmurs that seemed to rise from unseen depths. The air tasted of despair and decay, "
            "each breath a struggle. Time and direction vanished in the fog.<br>"
            ], next_state='main', on_complete=None)
            if any(item[0] == 'potion' for item in self.inventory):
                self.update_output("Use command 'use potion' to end game.<br>")
        
        elif location == 'elvira':
            self.click_through_text([
            "You are transported to a small, modest bedroom—the sanctuary of Antonia’s innocence and Elvira’s protection. The faint scent of flowers mingles with the crisp, clean air that "
            "flows through pale curtains swaying gently at the window. A soft glow from the candlestick on the wooden table flickers, casting warm light over the neatly made bed with its "
            "pristine white sheets, where Antonia lies peacefully asleep. The faint creak of the floor beneath you and the fragile clink of the rosary add to the stillness. Yet, the sweetness "
            "of the space is tainted by a heavy sadness, as if the room itself remembers the tragedy that will unfold.<br>",

            "<b>God:</b> This was a place of innocence, a refuge of love and devotion. Yet you, Ambrosio, turned it into a site of violence and betrayal. Look upon what was once whole, and see what you have destroyed.<br>",

            "The air thickens as the scene before you shifts. A memory begins to unfold, and you are forced to relive the moment of Elvira’s death. Her terrified voice fills the room as the events play out before your eyes:<br>",

            "“Terrified at the fury which flashed in his eyes, and at the tremendous threats which He uttered, Elvira sank upon her knees and besought his mercy in terms the most pathetic "
            "and touching. Unmoved by her sorrow and finding his threats unavailing, the Barbarian resolved to silence her complaints forever. Rushing upon her, He clasped his hands round "
            "her throat, and pressing it with his utmost strength, He persisted in his attempt till her voice was for ever silenced. Her lifeless and disfigured body fell motionless at his "
            "feet. He gazed upon it with horror. A frightful blackness spread itself over her visage; her limbs moved no more; the blood was chilled in her veins, and her heart had forgotten to beat.”<br>"
            "<i>(The Monk, Page 160)</i><br>",

            "The memory fades, and the room transforms. The bed is unmade, its sheets darkened by shadow. A shattered vase spills petals across the floor, symbols of innocence destroyed. "
            "Elvira’s lifeless body lies before you, her face consumed by a 'frightful blackness.'<br>",

            "<b>God:</b> Her face, marred by the blackness of death, reflects your betrayal and violence. This darkness is not only hers—it is the shadow of your soul. Look upon it and confront what you have done.<br>"
        ], next_state='main', on_complete=None)
        
        elif location == 'matilda':
            self.click_through_text([
            "You enter the monastery’s library, where dim candlelight dances across towering shelves of ancient books. The air is thick with the weight of past sins, "
            "carrying the faint scent of incense mingled with a darker, sour trace of decay. At the center stands a grand desk, draped in a sable cloth embroidered "
            "with golden symbols, its surface seeming to absorb the flickering light. The silence is oppressive, broken only by the distant creak of old wood, as "
            "though the room itself mourns what was lost here.<br>",

            "<b>God:</b> “Here is where your path began to twist, Ambrosio. Within these walls, you let yourself be blinded by her golden promises and consumed by the shadows she cast. "
            "Watch now, and see the truth of what you chose.”<br>",

            "The room grows brighter as a memory takes form. You see Matilda standing before you, cloaked in a long sable robe, the dark fabric flowing like a shadow across the floor. "
            "Her eyes gleam with power, and her voice is soft yet commanding:<br>",

            "“She was now cloathed in a long sable Robe, on which was traced in gold embroidery a variety of unknown characters. Her hair was loose and flowed wildly upon her shoulders; "
            "Her eyes sparkled with terrific expression; and her whole demeanor was calculated to inspire the beholder with awe and admiration.”<br>"
            "<i>(The Monk, Page 145)</i><br>",

            "Matilda speaks:<br>",

            "“You are meant for so much more than these vows, Ambrosio. Let go of your chains, and I will lead you to power and freedom beyond your imagination.”<br>",

            "The shadows of her robe spread through the room, dimming the light and suffocating the space in sable darkness.<br>",

            "<b>God:</b> The sable she wore was no mere garment, Ambrosio. It was the shadow of destruction, the darkness you allowed into your soul. See it now for what it was.<br>",

            "As the shadows fade, the golden embroidery on Matilda’s robe begins to glow, illuminating her flowing hair. The memory shifts, and you see her step closer, her golden hair "
            "gleaming in the candlelight, almost angelic in its brilliance.<br>",

            "“What was his amazement at beholding the exact resemblance of his admired Madona? The same exquisite proportion of features, the same profusion of golden hair, the same rosy lips, "
            "heavenly eyes, and majesty of countenance adorned Matilda!”<br>"
            "<i>(The Monk, Page 44)</i><br>",

            "<b>God:</b> You saw her golden beauty, her rosy cheeks, and her sable robe, and you chose them over your vows as a monk. You desired what was not yours to take, and in doing so, "
            "you broke My law. Tell me, Ambrosio: which commandment did you violate here?”<br>"
        ], next_state='main', on_complete=None)
        
        elif location == 'antonia':
            self.click_through_text([
                "The vision sharpens, revealing the bustling interior of the monastery’s chapel. The faint murmur of prayers and rustling robes fills the air, mingling with the heavy scent of incense. "
                "Among the congregation, Ambrosio’s gaze locks on Antonia. She stands beside her mother, her delicate figure framed by a flowing white gown fastened with a pale blue sash. Her golden ringlets "
                "cascade softly down her back, catching the warm glow of candlelight, and her face is veiled in quiet reverence. Her modest movements and downcast eyes exude an air of angelic purity.<br>",

                "<b>God:</b> Here is where you first saw her, Ambrosio. A soul filled with faith, her heart untainted by sin. But you did not see her devotion. You saw only her innocence, "
                "and in your heart, you sought to claim it.<br>",

                "His eyes lingered, drawn not to her prayer but to the fragile beauty that accompanied it. Her modesty, her reverence—each movement spoke of a soul untainted, yet to Ambrosio, "
                "they were invitations rather than virtues. She seemed almost unearthly, a vision set apart from the rest of the congregation, untouched by the world’s cruelties.<br>",

                "“It was of the most dazzling whiteness, and received additional charms from being shaded by the tresses of her long fair hair, which descended in ringlets to her waist. "
                "Her bosom was carefully veiled. Her dress was white; it was fastened by a blue sash, and just permitted to peep out from under it a little foot of the most delicate proportions.”<br>"
                "<i>(The Monk, pg 4)</i><br>",

                "<b>God:</b> You saw her white gown, her modesty, her gentle prayers. But instead of guiding her, you let your heart be consumed by covetous desire.<br>",

                "As her delicate figure shimmered in the soft light of the church, her innocence glowing like a beacon, the vision began to shift. The warmth of the chapel faded, and a suffocating darkness enveloped the space. "
                "The faint scent of incense was replaced by the damp, acrid stench of decay. You find yourself in the cold, oppressive confines of a tomb. Rough-hewn stone walls press inward, and the faint drip of water echoes "
                "through the silence, mingling with the muffled cries of distant anguish. A single torch flickers weakly, its light casting jagged shadows across the chamber.<br>",

                "Before you lies Antonia, trembling, her white gown now stained and torn, a fragile figure surrounded by darkness. The air feels heavy with dread, and her quiet sobs pierce the silence, pleading for mercy that will not come.<br>",

                "Then the memory sharpens, pulling you into the violent moment:<br>",

                "“Quickened by her cries, the sound of footsteps was heard approaching. The Abbot expected every moment to see the Inquisitors arrive. Antonia still resisted, and He now enforced her silence by means the most horrible and inhuman. "
                "He still grasped Matilda's dagger: Without allowing himself a moment's reflection, He raised it, and plunged it twice in the bosom of Antonia! She shrieked, and sank upon the ground. The Monk endeavoured to bear her away with him, "
                "but She still embraced the Pillar firmly. At that instant the light of approaching Torches flashed upon the Walls. Dreading a discovery, Ambrosio was compelled to abandon his Victim, and hastily fled back to the Vault, where He had left Matilda.”<br>"
                "<i>(The Monk, Page 204)</i><br>",

                "The vision lingers on Antonia’s lifeless form, her blood pooling on the cold stone floor, her once-white gown now soaked in red. The torchlight flickers as though struggling to endure the weight of the scene, "
                "casting her face into shadow—a haunting reminder of innocence stolen and a soul betrayed.<br>"
            ], next_state='main', on_complete=None)

    def start_main_game(self):
        # Transition to the main game loop
        self.update_output('Welcome to Creepy Monk!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to elvira\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: <b>\'purgatory\'</b> for Purgatory, <b>\'elvira\'</b> for Elvira\'s Apartment,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>\'matilda\'</b> Matilda in the Monestary, and <b>\'antonia\'</b> for Antonia\'s Tomb<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'grab\' followed by a reachable colour to grab the colour and add it to your inventory  (note, items are bolded)<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory, and all colours available to grab<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
        self.inventory.append(("empty canvas", get_resource_path("map.pdf")))
        self.enter_area('purgatory')  # Enter the initial location

    def show_pdf(self, pdf_path):
        """
        Show the given PDF file in the default system viewer.
        :param pdf_path: Relative file path to the PDF
        """
        full_path = get_resource_path(pdf_path)

        # Ensure the file exists
        if os.path.exists(full_path):
            # Open the PDF with the default system viewer
            os.system(f'open "{full_path}"')  # macOS/Linux
            # For Windows, use os.system(f'start "" "{full_path}"')
        else:
            self.update_output("<span style='color:black;'>PDF not found!</span><br>")

    def keyPressEvent(self, event):
        if self.game_state == 'reading':
            self.handle_reading_keypress()
            return

        # Default behavior for other key press events
        super().keyPressEvent(event)

    def click_through_text(self, text_array, next_state='main', on_complete=None):
        """
        Initiates a click-through text sequence, allowing the user to progress through an array of strings.

        :param text_array: List of strings to display sequentially.
        :param next_state: The game state to switch to after the sequence ends (default is 'main').
        :param on_complete: A callable function to execute after the sequence ends.
        """
        self.text_sequence = text_array  # Store the text sequence to display
        self.text_index = 0  # Start at the first text in the sequence
        self.next_state = next_state  # State to switch to after the sequence ends
        self.on_complete = on_complete  # Store the completion callback

        self.input_line.setEnabled(False)  # Disable input
        self.game_state = 'reading'  # Set game state to 'reading'

        # Display the first text and a prompt to continue
        self.update_output(self.text_sequence[self.text_index] + "<br>")
        self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")

    def handle_reading_keypress(self):
        """
        Handles keypress events during the 'reading' game state.
        Advances through the text sequence or ends the sequence if complete.
        """
        self.text_index += 1  # Move to the next text in the sequence

        if self.text_index < len(self.text_sequence):
            # Display the next text
            self.update_output(self.text_sequence[self.text_index] + "<br>")
            self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
        else:
            # End the sequence
            self.text_sequence = []  # Clear the text sequence
            self.text_index = 0  # Reset the index

            self.input_line.setEnabled(True)  # Re-enable input
            self.game_state = self.next_state  # Transition to the next state

            # Execute the callback if provided
            if self.on_complete:
                self.on_complete()

    def end_game_message(self):
        self.update_output("The story has concluded. Thank you for playing my game! You can now read over the story, or exit the game.<br>")
        self.input_line.setEnabled(False)  # Disable input field


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = AdventureGame()
    game.show()
    sys.exit(app.exec_())
