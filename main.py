import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QMainWindow, QSplitter
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtCore import Qt, QSize

class AdventureGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window size to 50% of the screen
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.6)
        height = int(screen.height() * 0.6)
        self.resize(width, height)

        self.setWindowTitle('Rappaccini\'s Garden - ReWritten By You')
        self.start_screen()

        self.game_state = 'start'  # Start in the 'start' phase
        self.workbench_step = 0  # Initialize the workbench step counter
        self.used_items = []
        self.end_paragraphs = []  # Placeholder for the ending sequence paragraphs
        self.end_paragraph_index = 0  # Index for the current paragraph in the ending sequence
        
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

        # Map locations to available items and their associated images
        self.location_items = {
            'Body': {'Anemones': 'anemones.pdf'},
            'Fountain': {'Pigweed': 'pigweed.pdf', 'Apple-Peru': 'appleperu.pdf'},
            'Statues': {'Moss': 'moss.pdf', 'Bachelors-Buttons': 'bachelorsbuttons.pdf'},
            'Gate': {'Cherry-Blossom': 'cherryblossom.pdf', 'Apple-Tree': 'appletree.pdf'},
            'Lab': {'Wild-Grapes': 'wildgrapevine.pdf', 'Sonnets': 'Sonnets.pdf'}
        }

        # Initialize locations
        self.locations = ['Body', 'Fountain', 'Statues', 'Gate', 'Lab']
        self.current_location = 'Body'  # Starting location

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

        # Set paragraphs for the intro phase
        self.intro_paragraphs = [
            "“Dear Beatrice,” said he, approaching her, while she shrank away as always at his approach, but now with a different impulse, "
            "“dearest Beatrice, our fate is not yet so desperate. Behold! there is a medicine, potent, as a wise physician has assured me, "
            "and almost divine in its efficacy. It is composed of ingredients the most opposite to those by which thy awful father has brought "
            "this calamity upon thee and me. It is distilled of blessed herbs. Shall we not quaff it together, and thus be purified from evil?”",

            "“Give it me!” said Beatrice, extending her hand to receive the little silver vial which Giovanni took from his bosom. She added, "
            "with a peculiar emphasis, “I will drink; but do thou await the result.”",

            "She put Baglioni’s antidote to her lips; and, at the same moment, the figure of Rappaccini emerged from the portal and came slowly "
            "towards the marble fountain. As he drew near, the pale man of science seemed to gaze with a triumphant expression at the beautiful youth "
            "and maiden, as might an artist who should spend his life in achieving a picture or a group of statuary and finally be satisfied with his success. "
            "He paused; his bent form grew erect with conscious power; he spread out his hands over them in the attitude of a father imploring a blessing upon "
            "his children; but those were the same hands that had thrown poison into the stream of their lives. Giovanni trembled. Beatrice shuddered nervously, "
            "and pressed her hand upon her heart.",

            "“My daughter,” said Rappaccini, “thou art no longer lonely in the world. Pluck one of those precious gems from thy sister shrub and bid thy bridegroom "
            "wear it in his bosom. It will not harm him now. My science and the sympathy between thee and him have so wrought within his system that he now stands "
            "apart from common men, as thou dost, daughter of my pride and triumph, from ordinary women. Pass on, then, through the world, most dear to one another "
            "and dreadful to all besides!”",

            "“My father,” said Beatrice, feebly,—and still as she spoke she kept her hand upon her heart,—“wherefore didst thou inflict this miserable doom upon thy child?”",

            "“Miserable!” exclaimed Rappaccini. “What mean you, foolish girl? Dost thou deem it misery to be endowed with marvellous gifts against which no power nor strength "
            "could avail an enemy—misery, to be able to quell the mightiest with a breath—misery, to be as terrible as thou art beautiful? Wouldst thou, then, have preferred "
            "the condition of a weak woman, exposed to all evil and capable of none?”",

            "“I would fain have been loved, not feared,” murmured Beatrice, sinking down upon the ground. “But now it matters not. I am going, father, where the evil which thou "
            "hast striven to mingle with my being will pass away like a dream—like the fragrance of these poisonous flowers, which will no longer taint my breath among the flowers of Eden. "
            "Farewell, Giovanni! Thy words of hatred are like lead within my heart; but they, too, will fall away as I ascend. Oh, was there not, from the first, more poison in thy nature than in mine?”",

            "To Beatrice,—so radically had her earthly part been wrought upon by Rappaccini’s skill,—as poison had been life, so the powerful antidote was death; and thus the poor victim "
            "of man’s ingenuity and of thwarted nature, and of the fatality that attends all such efforts of perverted wisdom, perished there, at the feet of her father and Giovanni. "
            "Just at that moment Professor Pietro Baglioni looked forth from the window, and called loudly, in a tone of triumph mixed with horror, to the thunderstricken man of science, "
            "“Rappaccini! Rappaccini! and is this the upshot of your experiment!”",

            "- The above was text from Nathaniel Hawthornes \"Rappacini's Daughtere\""

            "The garden, rich with its strange and terrible beauty, seemed to hold its breath. The vibrant hues of its blossoms—so like flames, jewels, and the very blood of life—were dimmed beneath "
            "a shadow that had fallen upon this unnatural paradise. The marble fountain murmured faintly, its voice subdued, while the vines that clung to statues and crept along the paths appeared "
            "to writhe faintly, as if stirred by some unseen agony.",

            "Beatrice lay motionless upon the cold earth, her luscious locks, laced with white flowers, fanned out like a dark crown around her, her radiant vitality extinguished, as though the very garden "
            "that had nurtured her life now grieved her passing. Dame Lisabetta had flung herself to her knees, her cries rising in uneven bursts as she clutched at the still form of the maiden, her grief raw "
            "and unrestrained. Dr. Rappaccini, spectral and bent, moved about the garden like a man lost to his own thoughts, his pacing erratic, his face a pale mask of anguish or calculation.",

            "In the midst of his frantic movements, the doctor turned sharply, and from the folds of his coat fell two slips of paper. They drifted to the ground, unheeded by him, catching the faint air stirred by "
            "his motion. With a strange compulsion, you step forward and pick them up. One is a map, crudely sketched, its lines marking the twisting paths and hidden corners of the garden with a precision that "
            "hinted at secret purposes. The other is a letter, addressed in a trembling hand to Beatrice, its words trailing off into an unfinished silence. What secrets it might reveal were now left to the stillness "
            "of the garden and the unanswered questions that hung heavy in the air.",

            "The letter reads:",

            "My Dearest Beatrice,<br><br>"
            "The weight of my deeds grows heavier with each passing day. In my pursuit of knowledge, I have become blind to the line between creation and destruction. Science has made me cruel, and in its name, I have "
            "turned you, my beloved daughter, into a monster.<br>"
            "Yet, even as I wrought this terrible fate upon you, I have worked in secret to undo it. Among the flowers of this garden, I have grown those with the power to heal, to cleanse the poison I placed within "
            "you. It was my dream that one day, you would be free from the shadow of my ambition, able to walk among your kind as you were meant to.<br>"
            "Forgive me, if forgiveness is possible. If not, may the remedy I have labored to create serve as my atonement. My love for you, though flawed and burdened by guilt, has never faltered...<br><br>"
            "Your father,<br>Giacomo Rappaccini"
        ]

        self.current_paragraph = 0  # Initialize paragraph counter

        # Disable input during the intro phase
        self.input_line.setEnabled(False)

        # Display the first paragraph and prompt
        self.update_output(self.intro_paragraphs[self.current_paragraph] + "<br>")
        self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")

        # Set initial game state to 'intro'
        self.game_state = 'intro'

    def update_output(self, text, image_path=None):
        self.output_area.moveCursor(QTextCursor.End)
        if image_path:
            self.output_area.insertHtml(f'<img src="{image_path}" width="300"><br>')
        else:
            self.output_area.insertHtml(f'{text}<br>')
        self.output_area.moveCursor(QTextCursor.End)

    def process_input(self):
        user_input = self.input_line.text().strip()
        self.input_line.clear()

        if not user_input:
            return

        # Display the user input in grey
        if user_input:  # Only display if input is not empty
            self.update_output(f"<span style='color:gray;'>{user_input}</span><br>")

        if self.game_state == 'intro':
            # Handle paragraphs during the intro phase
            self.current_paragraph += 1
            if self.current_paragraph < len(self.intro_paragraphs):
                self.update_output(self.intro_paragraphs[self.current_paragraph] + "<br>")
                self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
            else:
                # Transition directly to the main game
                self.start_main_game()
                self.game_state = 'main'
                self.input_line.setEnabled(True)  # Enable input for the main game

            return

        # If in main game state, process the main game commands
        if self.game_state == 'main':
            # Split command into parts, handle multiple spaces
            parts = user_input.split()
            command = parts[0].lower() if parts else ""

            # Validate the command
            valid_commands = ['show', 'list', 'grab', 'help', 'move', 'current', 'use', 'examine']
            if command not in valid_commands:
                self.update_output(f'<span style="color:black;">{command} is not a valid command.</span><br>')
                return
            
            if self.current_location == 'Lab':
                # Check for 'use workbench' command
                if command == 'use' and len(parts) > 1 and parts[1].lower() == 'workbench':
                    if len([item for item in self.inventory if item[0] not in ['Map', 'Sonnets', 'Potion']]) < 4:
                        self.update_output("It seems like you do not have enough items to create a potion.<br>")
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
                    self.update_output("Invalid syntax. Use 'use workbench' to interact with the workbench in the Lab.<br>")
                    return

            if command == 'use' and len(parts) > 1 and parts[1].lower() == 'potion':
                if any(item[0] == 'Potion' for item in self.inventory):
                    if self.current_location == 'Body':
                        self.game_state = 'end_sequence'  # Transition to the ending sequence state
                        self.end_paragraphs = [
                            # Add the provided paragraphs here
                            "You stand over Beatrice's still form, the enormity of what you’re about to do weighs heavy.<br>",

                            "With the vial tilted, the potion flows into Beatrice’s closed eyes, its gleaming liquid catching the dim light as it pools delicately on her lids. The garden seems to "
                            "hold its breath, a dense stillness gathering as though Nature herself dares not intrude. Slowly, the potion seeps into her flesh, gliding over the whites of her eyes "
                            "with an almost otherworldly radiance, as though it carries within it some long-forbidden hope.<br>",

                            "For a moment, all is silent. Then, with a sudden gasp, her chest rises sharply, and the air fills with the sound of life being pulled from the abyss. Her breaths come "
                            "in desperate, uneven bursts, each one breaking the suffocating quiet that surrounded her lifeless form. The veins that once twisted like dark tendrils beneath her skin "
                            "begin to vanish, receding as though banished by the light of dawn. Her pallor softens, not with the unearthly whiteness of death but with a luminous, delicate flush, her "
                            "alabaster skin now imbued with the faint blush of returning vitality. Her lips, no longer stained by death’s cruel tint, bloom into a soft pink, a quiet promise of her restoration.<br>",

                            "Around her, the garden trembles in response. A fetid odor rises as the poisonous blooms recoil from her rebirth, their vibrant hues fading to ashen black. Leaves curl "
                            "inward, vines shrivel, and the garden’s corrupt heart begins to crumble under the weight of its own undoing. The air, once heavy and cloying, seems to lift as the garden "
                            "exhales its death throes, its dark dominion collapsing into brittle ruin.<br>",

                            "Beatrice stirs, her trembling frame lifting as she sits upright. Her eyes, now clear and bright, meet yours with a look of astonishment, her gaze a fragile bridge between "
                            "life regained and the shadows she left behind. But suddenly, she doubles over, a deep, guttural sound escaping her as her body heaves. From her mouth pours a dark, viscous "
                            "slime, its green hue unnatural and sickly, pooling at her knees in thick, glistening streams. The acrid scent fills your nostrils, sharp and unbearable, yet she retches again "
                            "and again, as though expelling the very essence of the curse that held her.<br>",
                            
                            "When the convulsions cease, she remains hunched, her breaths shallow but steady. Her hands tremble as she raises herself once more. In the dim light, her pale skin glows faintly, "
                            "porcelain-like, but alive. Her cheeks, faintly flushed, contrast with the stark purity of her visage, her beauty now untainted by the poison’s mark. White tears streak her face, "
                            "shining like crystalline drops, each one catching the light with a dazzling brilliance. These tears, silent and serene, trace her cheeks as if her soul weeps softly for all that was "
                            "lost. Yet within those luminous streaks is a testament—not of despair, but of rebirth, of innocence reclaimed through pain’s bitter trial. She looks to you, her lips parting "
                            "slightly, though no words come, and in her gaze rests both gratitude and the lingering shadow of all she has endured.<br>",

                            "As you rise from your place beside Beatrice, still shaken by the enormity of what has just transpired, a shadow falls across the garden’s fading light. You turn to see Dr. Rappaccini "
                            "standing amidst the withered vines and crumbling blooms, his once-commanding figure now stooped and hollowed, his face etched with the weariness of a man who has carried his sins "
                            "too long. His eyes, sharp yet dulled by sorrow, linger on Beatrice—his creation, his masterpiece, his victim.<br>",

                            "He steps closer, his voice low and strained, yet carrying the weight of unspoken years. \"You have done what I could not,\" he says, his tone neither wholly bitter nor entirely grateful. "
                            "\"You have given her what my science stole—a life unshackled from the garden's curse.\"<br>",

                            "For a moment, he is silent, his gaze sweeping over the shriveled remains of the garden, a kingdom undone. Then, with an almost reverent gravity, he begins to speak—not in prose, but in "
                            "verse, the rhythm of his words resonating like a final confession:<br>",

                            "SONNET III: Rappaccini's Monologue<br><br>"
                            "I fell as lightning from the heavens’ height,<br>"
                            "Once crowned with wisdom, now a shadowed name,<br>"
                            "The Son of Morning, scorched by holy flame,<br>"
                            "Condemned to walk where truth gives way to blight.<br><br>"
                            "The serpent’s coil science, in hindsight,<br>"
                            "It whispered pride, my heart’s unholy claim,<br>"
                            "Its lure, forbidden, wove my soul in shame,<br>"
                            "And led me far from grace’s guiding light.<br><br>"
                            "In Beatrice, my pride sought twisted bloom,<br>"
                            "A fragile life remade through poisoned art,<br>"
                            "A mirror to my fall, her beauty’s doom.<br>"
                            "Yet from her tears, redemption’s tides must start,<br>"
                            "The garden dies, its thorns consumed by gloom,<br>"
                            "While she ascends to cleanse her father’s heart.<br><br>"
                        ]
                        self.end_paragraph_index = 0  # Reset the paragraph index
                        self.update_output(self.end_paragraphs[self.end_paragraph_index] + "<br>")
                        self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
                    else:
                        self.update_output("The potion is meant for Beatrice's body. Move to her location first.<br>")
                else:
                    self.update_output("You do not have a potion in your inventory.<br>")
                return

            # Handle 'help' command
            if command == 'help':
                if self.game_state == 'workbench':
                    self.update_output("You are using the workbench to create a potion. Follow the prompts to select items from your inventory.<br>")
                    return

                self.update_output('Welcome to Rappaccini\'s Garden!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to Gate\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: \'Body\' for Beatrice\'s Body, \'Lab\' for Dr. Rappaccini\'s Lab, \'Gate\' for The Secret Gate,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\'Fountain\' for The Broken Marble Fountain, and \'Statues\' for The Statues Covered With Overgrown Foliage<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'show \' followed by a item currently held in inventory to view the item. Ex. \'show oobi\'<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory<br>' +
                            'Use command \'grab\' followed by a reachable item to grab the item and add it to your inventory<br>' +
                            'Use command \'use potion\' near Beatrice\'s body, if potion has been aquired, to use the potion on Beatrice<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
                if self.current_location == 'Body':
                    self.update_output("Extra command: Use the command 'examine' followed by 'hands', 'shoes', or 'face' to inspect specific parts of Beatrice's body.<br>")
                if self.current_location == 'Lab':
                    self.update_output("Extra command: You can use the workbench by typing 'use workbench'. Make sure you have at least 4 items in your inventory.<br>")
                return

            # Handle 'current location' command
            if command == 'current' and len(parts) > 1 and parts[1].lower() == 'location':
                self.update_output(f"You are currently at {self.current_location}.<br>")
                return
            elif command == 'current':
                self.update_output("Invalid syntax. Use 'current location'.<br>")
                return

            if command == 'examine' and self.current_location == 'Body':
                if len(parts) < 2:
                    self.update_output("You must specify what to examine: 'hands', 'shoes', or 'face'.<br>")
                    return

                target = parts[1].lower()
                if target == 'hands':
                    self.update_output("Her hands lie unnaturally beside her, pale and slender, their stillness betraying the agony of her passing. "
                                    "The tips of her fingers are stained a deep purple, the veins beneath her skin like dark, creeping roots, a final sign of "
                                    "the poison that claimed her life. Her passing, you feel, was one of suffering and despair, a cruel culmination to a life lived "
                                    "in isolation and longing.<br>")
                elif target == 'shoes':
                    self.update_output("Her white shoes, though simple and beautiful, are marked with scuffs at the toes, a reminder of the countless steps she took in this garden—"
                                    "her sanctuary and her prison. They rest now as silent witnesses to her wandering and toil, an echo of her humanity amidst the garden’s strange "
                                    "and deadly beauty.<br>")
                elif target == 'face':
                    self.update_output("Her face, once so radiant with life, is pale as marble, her lips tinged with the same unnatural purple as her fingers. Along her jawline, faint "
                                    "green veins spread like delicate vines, creeping reminders of the poison that flowed through her. From the corners of her closed eyes, <b>green tears</b> "
                                    "spill down her pale cheeks, vivid and unnaturally vibrant against her ashen skin. Where they fall, they leave faint, darkened trails, as though the poison "
                                    "within them stains everything it touches. Around the spots where the tears have pooled, the skin turns purple and shadowed, veins spreading outward in "
                                    "delicate, haunting patterns, like the roots of some poisonous plant burrowing into the earth. These tears, more than mere sorrow, seem to carry the essence "
                                    "of the garden itself—beautiful, deadly, and beyond comprehension.<br>")
                    self.update_output("The compulsion grows too strong to resist. Your hands, trembling slightly, reach into your belongings and retrieve a small test tube with a tight-fitting cap. The air "
                                        "around Beatrice’s tears is thick with the floral sweetness, making your eyes water anew as you lean closer. Carefully, you tilt her face just enough to let the thick, "
                                        "jade-green drops flow into the glass.<br>")
                    self.update_output("The liquid pools at the bottom of the test tube, gleaming unnaturally as though it holds a life of its own. The floral scent intensifies for a moment, so sharp and "
                                        "cloying it feels as though it might drown you, before subsiding as you seal the tube tightly with the cap. The burning on your cheeks lingers, but there’s a strange "
                                        "satisfaction in holding this fragile vessel of her essence.<br>")
                    self.update_output("You slip the test tube into your pocket, its weight a quiet reminder of the choice you’ve made. The tears, so beautiful and haunting, are now yours to carry, though the "
                                        "thought lingers: what price might come with preserving the remnants of her poisoned sorrow?<br>")
                    self.update_output("Her dark hair, lustrous and beautiful, frames her face in soft waves, each strand a testament to the care she took even in the midst of her tragic existence. Braided "
                                        "among the strands are delicate white <b>anemones</b>, their sharp, musky scent cutting through the air. They lie nestled like a crown upon her head, their stark whiteness "
                                        "adding a haunting elegance to her repose. Yet something about them seems deliberate, a hidden intention woven into their placement.<br>")
                    self.update_output("The garden, alive with vibrant color and intoxicating fragrance, seems to hold its breath. Beatrice, once the heart of this place, now rests in its embrace, her stillness "
                                        "both beautiful and terrible.<br>")
                    self.update_output("You have added \'Green-Tears\' to your inventory.<br>")
                    self.inventory.append(("Green-Tears", "greentears.pdf"))
                    self.show_pdf("greentears.pdf")
                else:
                    self.update_output("You cannot examine that. Try 'hands', 'shoes', or 'face'.<br>")
                return

            # Handle 'grab' command
            if command == 'grab':
                if len(parts) < 2:
                    self.update_output('<span style="color:black;">An item must follow the command \'grab\'.</span><br>')
                else:
                    item = " ".join(parts[1:])  # Combine remaining parts into the item name
                    
                    # Check items available in the current location
                    available_items = self.location_items.get(self.current_location, {})
                    if item in available_items:
                        # Safely retrieve the file name
                        image_file = available_items[item]
                        
                        # Add item to inventory and remove from location
                        self.inventory.append((item, image_file))  # Store as (item_name, file_name)
                        del self.location_items[self.current_location][item]

                        self.update_output(f'<span style="color:black;">User grabbed {item}.</span><br>')
                        
                        # Automatically display the item after grabbing
                        self.show_pdf(image_file)

                    elif any(i[0] == item for i in self.inventory):
                        self.update_output(f'<span style="color:black;">{item} is already in your inventory!</span><br>')
                    else:
                        self.update_output(f'<span style="color:black;">There is no item {item} to grab at this location.</span><br>')
                return

            # Handle 'list items' command
            if command == 'list':
                if len(parts) == 2 and parts[1].lower() == 'items':
                    # List inventory items
                    if self.inventory:
                        inventory_items = ', '.join(item[0] for item in self.inventory)
                        self.update_output(f'<span style="color:black;">Items in your inventory: {inventory_items}</span><br>')
                    else:
                        self.update_output('<span style="color:black;">Your inventory is empty.</span><br>')
                    
                    # List available items at the current location
                    location_items = self.location_items.get(self.current_location, {})
                    if location_items:
                        location_items_list = ', '.join(location_items.keys())
                        self.update_output(f'<span style="color:black;">Items available at this location: {location_items_list}</span><br>')
                    else:
                        self.update_output('<span style="color:black;">No items available to grab at this location.</span><br>')
                    return
                else:
                    self.update_output(f'<span style="color:black;">{user_input} is not a valid command.</span><br>')
                    return

            # Handle 'show' command
            if command == 'show':
                if len(parts) < 2:
                    self.update_output('<span style="color:black;">An item must follow the command \'show\'.</span><br>')
                else:
                    item = " ".join(parts[1:])  # Combine remaining parts into the item name
                    # Check if the item is in the inventory
                    for inv_item, image_file in self.inventory:
                        if inv_item == item:
                            self.update_output(f'<span style="color:black;">Showing {item}.</span><br>')
                            self.show_pdf(image_file)  # Show the corresponding image
                            return
                    self.update_output(f'<span style="color:black;">You do not have {item} in your inventory.</span><br>')
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
                if any(item[0] == base and base not in self.used_items and item[0] not in ['Potion', 'Sonnets', 'Map'] for item in self.inventory):
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
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show Sonnets\'<br>")
                return

            if self.workbench_step == 2:
                ingredient1 = user_input.strip()
                if any(item[0] == ingredient1 and ingredient1 not in self.used_items and item[0] not in ['Potion', 'Sonnets', 'Map'] for item in self.inventory):
                    self.selected_ingredient1 = ingredient1
                    self.used_items.append(ingredient1)  # Mark ingredient as used
                    self.update_output(f"You added {ingredient1} to the potion.<br>")
                    self.workbench_step = 3
                    self.update_output("Please enter the second ingredient:<br>")
                    self.list_inventory()  # Show available items
                else:
                    self.update_output(f"{ingredient1} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show Sonnets\'<br>")
                return

            if self.workbench_step == 3:
                ingredient2 = user_input.strip()
                if any(item[0] == ingredient2 and ingredient2 not in self.used_items and item[0] not in ['Potion', 'Sonnets', 'Map'] for item in self.inventory):
                    self.selected_ingredient2 = ingredient2
                    self.used_items.append(ingredient2)  # Mark ingredient as used
                    self.update_output(f"You added {ingredient2} to the potion.<br>")
                    self.workbench_step = 4
                    self.update_output("Please enter the third ingredient:<br>")
                    self.list_inventory()  # Show available items
                else:
                    self.update_output(f"{ingredient2} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show Sonnets\'<br>")
                return

            if self.workbench_step == 4:
                ingredient3 = user_input.strip()
                if any(item[0] == ingredient3 and ingredient3 not in self.used_items and item[0] not in ['Potion', 'Sonnets', 'Map'] for item in self.inventory):
                    self.selected_ingredient3 = ingredient3
                    self.used_items.append(ingredient3)  # Mark the ingredient as used

                    # Check if the recipe is correct
                    correct_base = "Green-Tears"
                    correct_ingredients = {"Anemones", "Pigweed", "Moss"}

                    # Verify the base and the selected ingredients
                    if (self.selected_base == correct_base and
                        {self.selected_ingredient1, self.selected_ingredient2, self.selected_ingredient3} == correct_ingredients):
                        # Success case
                        self.update_output("The potion is ready, its surface glowing faintly as though alive with hope—or perhaps something far more perilous. "
                                        "In your hands lies the culmination of your efforts, the chance to undo the poison that claimed Beatrice’s life.<br>")
                        self.inventory.append(("Potion", "potion.pdf"))  # Add potion to inventory
                        self.show_pdf("potion.pdf")  # Open the potion PDF
                        self.update_output("You can now try using the potion on Beatrice's body.<br>")
                    else:
                        # Failure case
                        self.update_output("The beaker begins to bubble uncontrollably, steam rising in angry hisses as the mixture turns an ominous, murky color. "
                                        "Suddenly, with a deafening POP, the concoction explodes upward, splattering scalding liquid and noxious fumes into the air.<br>")
                        self.update_output("Try again using different ingredients, or go out and search for more.<br>")
                        self.update_output("You can try by typing 'use workbench', or go to a different location using a 'move to' command.<br>")

                    # Reset workbench state after the attempt
                    self.used_items = []  # Reset used items for the next session
                    self.workbench_step = 0  # Reset step counter
                    self.game_state = 'main'  # Return to the main game state
                else:
                    self.update_output(f"{ingredient3} is either not in your inventory or has already been used.<br>")
                    self.update_output("You may use command 'list items' to list inventory or command 'show' followed by an item to view it. Hint, you may want to use \'show Sonnets\'<br>")
                return

    def list_inventory(self):
        available_items = [item[0] for item in self.inventory if item[0] not in self.used_items and item[0] not in ['Potion', 'Sonnets', 'Map']]
        if available_items:
            inventory_items = ', '.join(available_items)
            self.update_output(f"Your available inventory: {inventory_items}<br>")
        else:
            self.update_output("No items are currently available for selection.<br>")

    def enter_area(self, location):
        self.current_location = location

        if location == 'Body':
            full_location = 'Beatrice\'s Body'
        elif location == 'Fountain':
            full_location = 'The Broken Marble Fountain'
        elif location == 'Statues':
            full_location = 'The Statues Covered With Overgrown Foliage'
        elif location == 'Gate':
            full_location = 'The Secret Gate'
        elif location == 'Lab':
            full_location = 'Dr. Rappaccini\'s Lab'

        self.update_output(f"You have walked to {full_location}.<br>")

        if location == 'Body':
            self.update_output("At the very heart of the garden, where the plants seem most alive with unnatural vigor, "
                            "Beatrice lies motionless, her form radiant even in death. She rests upon the earth as though "
                            "the garden itself has claimed her, the vibrant life around her mocking the stillness of her body. "
                            "Dame Lisabetta kneels beside her, weeping softly, her frail hands clutching the folds of Beatrice’s "
                            "dress as if to hold her closer to the world she has left behind.<br><br> Use the command 'examine' "
                            "followed by 'hands', 'shoes', or 'face' to inspect specific parts of Beatrice's body.<br>")
            if 'Potion' in self.inventory:
                self.update_output("Use command 'use potion' to use the potion on Beatrice.<br>")
        elif location == 'Fountain':
            self.update_output("The broken fountain stands to the side of the garden, a silent relic of its former grandeur. "
                            "Its fractured marble still holds a quiet dignity, though the water that trickles from its damaged spout "
                            "seems to sustain not beauty, but invasion. Two plants have taken root nearby, their presence bold and unyielding.<br>")
            self.update_output("The coarse, sprawling <b>pigweed</b> creeps close, its thick leaves seeming to sap life from the fountain’s soil. "
                            "Beside it, the ghostly <b>apple-peru</b>, with its thorned stems and pale, bell-shaped flowers, leans as though "
                            "drawn to the fountain’s water. These invasive plants thrive here, leaching from the broken structure, their "
                            "relentless growth a mockery of the fountain’s once-pristine form.<br>")
        elif location == 'Statues':
            self.update_output("You approach a secluded corner of the garden, where ancient statues rise from the earth, their forms veiled "
                            "in layers of thick <b>moss</b>. The soft, green growth clings to the stone like an aged memory, its earthy, woody scent "
                            "mingling with the dampness of the air. The statues are barely recognizable, their features eroded by time and now "
                            "obscured by nature’s relentless touch. This overgrowth, symbolic of decay and renewal, renders the statues ghostlike, "
                            "blending them into the landscape.<br>")
            self.update_output("At the base of the statues, a bed of <b>bachelor’s buttons</b> spreads, their deep blue and purple blooms forming a luscious "
                            "carpet. Their mild, earthy fragrance contrasts with the sharp tang of the moss, creating a peculiar harmony. The flowers "
                            "thrive in wild abundance, as though the statues themselves have nurtured this beauty amidst the ruin.<br>")
            self.update_output("This place feels alive yet somber, the moss and flowers combining to create a scene of quiet reverence, where nature has "
                            "reclaimed what was once the work of man.<br>")
        elif location == 'Gate':
            self.update_output("The Secret Gate, the one Dame Lisabetta once revealed to you, stands hidden at the edge of the garden, cloaked in the wild "
                            "embrace of overgrowth. Its iron bars, once strong and imposing, are now weathered by time and nearly swallowed by the trees that "
                            "guard it. The delicate limbs of a <b>cherry blossom tree</b> arch gracefully over the gate, its pale pink and white blossoms scattering "
                            "petals onto the path below. Their fleeting beauty seems almost to mourn the secrets the gate keeps locked away. The air is sweet "
                            "with their faint floral scent, tinged by the bitterness of their inevitable fall.<br>")
            self.update_output("Beside it grows an <b>apple tree</b>, its gnarled branches twisted in forms that seem almost human, stretching toward the gate as if in longing. "
                            "The bark, dark and rough, is streaked with moss, while its boughs bear fruit—apples sweet yet tinged with a bittersweet aroma, as though they "
                            "carry the weight of forgotten stories. The tree’s contorted shape and lingering vitality evoke a haunting sense of time’s passage, its presence "
                            "both somber and enduring.<br>")
            self.update_output("These trees, intertwined and resolute, shield the gate as if conspiring with it to conceal what lies beyond. Their beauty, at once serene and "
                            "unsettling, reminds you of the garden’s strange balance between life and decay.<br>")
        elif location == 'Lab':
            self.update_output("At the northernmost edge of the garden, concealed beneath the wild embrace of overgrowth, lies Dr. Rappaccini’s lab. The small, weathered "
                            "structure is nearly swallowed by the garden’s relentless life. Its wooden door hangs askew, broken and splintered, its strength eroded by time "
                            "and neglect. Wild <b>grapes</b> coil tightly across its surface, their dark leaves thick and glossy, their clusters of grapes hanging heavy like "
                            "forgotten ornaments.<br>")
            self.update_output("The grapes catch your eye, their rich, deep purple mirroring the hue of Beatrice’s fingertips and lips—a haunting reminder of the poison that "
                            "consumed her. They glisten faintly, their thin skins taut and unbroken, exuding a faintly sour aroma that mixes with the sharper chemical tang "
                            "emanating from within the lab. The vines twist and cling to the doorframe as if alive, their tendrils curling with an almost deliberate intent "
                            "to shield the secrets beyond.<br>")
            self.update_output("The air here is heavy with unease, the scent of fermenting grapes and faint decay mingling in a way that makes you hesitate. Yet the door, though "
                            "nearly hidden, stands ajar, offering you the chance to uncover what lies within.<br>")
            self.update_output("At the workbench, amidst the scattered papers stained with chemical spills and hurried scrawls, one sheet catches your attention. Its edges are "
                               "singed, as though it had once come dangerously close to an open flame, yet the writing is unmistakably deliberate. Unlike the other notes and "
                               "scribbles, this one is crafted with care, written in elegant, looping script.<br>")
            self.update_output("As you step into the lab, a sharp, chemical tang fills the air, mingling with the damp, earthy scent of the wild garden just outside. The space "
                               "is dimly lit, its windows clouded with dust and streaks of dried condensation, allowing only faint beams of light to penetrate the gloom. The "
                               "room is a chaotic mess: bottles and vials are scattered across every surface, some empty, others half-filled with liquids of strange and "
                               "unsettling hues. Papers and notes, yellowed with age, lie in disarray, their faded script hinting at experiments long abandoned.<br>")
            self.update_output("At the far side of the room, a sturdy fume hood looms, its contents locked behind glass. Rows of chemicals are visible inside, neatly organized "
                               "but frustratingly out of reach. A lock secures the cabinet tightly, and you have no key. Whatever lies within remains an enigma, for now.<br>")
            self.update_output("In the center of the room stands a workbench, the one area that retains a semblance of order. A variety of lab equipment is neatly arranged: "
                               "beakers, a Bunsen burner, tongs, titrants, and stands with stopcocks and clamps. Everything needed for precise work awaits you, though the "
                               "bench’s surface is stained with the remnants of past experiments—dark rings where flasks once stood, and faint scorch marks that hint at trials "
                               "gone wrong.<br>")
            self.update_output("At the workbench, amidst the scattered papers stained with chemical spills and hurried scrawls, one sheet catches your attention. Its edges are "
                               "singed, as though it had once come dangerously close to an open flame, yet the writing is unmistakably deliberate. Unlike the other notes and "
                               "scribbles, this one is crafted with care, written in elegant, looping script.<br>")
            self.update_output("The words are arranged in two poems of fourteen lines, their rhythm and rhyme unmistakable: Petrarchan <b>sonnets</b>, their form popular in the Romantic period. "
                               "The carefully constructed lines suggest that this is no ordinary note—it must hold the secret to Dr. Rappaccini’s antidote. The clever disguise "
                               "of poetry was likely meant to ensure only someone as determined and intuitive as you could uncover its meaning.<br>")
            self.update_output("Use command '<b>use workbench</b>' to use the workbench.<br>")

    def start_main_game(self):
        # Transition to the main game loop
        self.update_output('Welcome to Rappaccini\'s Garden!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to Gate\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: \'Body\' for Beatrice\'s Body, \'Lab\' for Dr. Rappaccini\'s Lab, \'Gate\' for The Secret Gate,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\'Fountain\' for The Broken Marble Fountain, and \'Statues\' for The Statues Covered With Overgrown Foliage<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'show \' followed by a item currently held in inventory to view the item. Ex. \'show oobi\'<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory<br>' +
                            'Use command \'grab\' followed by a reachable item to grab the item and add it to your inventory<br>' +
                            'Use command \'use potion\' near Beatrice\'s body, if potion has been aquired, to use the potion on Beatrice<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
        self.inventory.append(("Map", "map.pdf"))
        self.show_pdf("map.pdf")
        self.enter_area('Body')  # Enter the initial location

    def show_pdf(self, pdf_path):
        # Ensure the file exists
        if os.path.exists(pdf_path):
            # Open the PDF with the default system viewer
            os.system(f'open "{pdf_path}"')  # macOS/Linux
            # For Windows, replace with os.system(f'start "" "{pdf_path}"')
        else:
            self.update_output("<span style='color:black;'>PDF not found!</span><br>")

    def keyPressEvent(self, event):
        if self.game_state == 'intro':
            # Handle the intro paragraphs (already working correctly)
            self.current_paragraph += 1
            if self.current_paragraph < len(self.intro_paragraphs):
                self.update_output(self.intro_paragraphs[self.current_paragraph] + "<br>")
                self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
            else:
                # Transition directly to the main game
                self.start_main_game()
                self.game_state = 'main'
                self.input_line.setEnabled(True)  # Enable input for the main game
            return
        
        if self.game_state == 'end_sequence':
            self.end_paragraph_index += 1
            if self.end_paragraph_index < len(self.end_paragraphs):
                self.update_output(self.end_paragraphs[self.end_paragraph_index] + "<br>")
                self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
            else:
                self.update_output("The story has concluded. Please exit the game.<br>")
                self.input_line.setEnabled(False)  # Disable input field
                self.game_state = 'ended'  # Final state to prevent further actions
            return

        # Default behavior for other key press events
        super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = AdventureGame()
    game.show()
    sys.exit(app.exec_())
