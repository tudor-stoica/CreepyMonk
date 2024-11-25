import sys
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
        self.ungrabbed_items = ['oobi pic', 'chill']  # Items available to grab
        
        # Create a splitter to dynamically resize top and bottom sections
        self.splitter = QSplitter(Qt.Vertical)
        
        # Output area (80% of height)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #CDEBC5; color: black; padding-left: 10px;")
        self.splitter.addWidget(self.output_area)


        # Input area (20% of height)
        self.input_line = QLineEdit()
        self.input_line.setMaxLength(20)
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

        # Set initial game state
        self.game_state = 'start'
        self.update_output('Welcome to Rappaccini\'s Garden!<br><br>' +
                           'Instructions:<br>' + 
                           'Use commmand \'move\' followed by a reachable location to move there. Ex. \'move Secret Gate\'<br>' +
                           'Use command \'current location\' to print out the current location of the player<br>' +
                           'Use command \'show \' followed by a item currently held in inventory to view the item. Ex. \'show oobi\'<br>' +
                           'Use command \'list items\' to print out a list of all items held in the inventory<br>' +
                           'Use command \'grab\' followed by a reachable item to grab the item and add it to your inventory<br>' +
                           'Use command \'help\' to print out these instructions once again<br><br>')

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

        # Do nothing for empty or space-only input
        if not user_input:
            return

        # Print user's input in grey color
        self.update_output(f'<span style="color:gray;">{user_input}</span><br>')

        # Split command into parts, handle multiple spaces
        parts = user_input.split()
        command = parts[0].lower() if parts else ""

        # Validate the command
        valid_commands = ['show', 'list', 'grab']
        if command not in valid_commands:
            self.update_output(f'<span style="color:black;">{command} is not a valid command.</span><br>')
            return

        # Handle 'grab' command
        if command == 'grab':
            if len(parts) < 2:
                self.update_output('<span style="color:black;">An item must follow the command \'grab\'.</span><br>')
            else:
                item = " ".join(parts[1:])  # Combine remaining parts into the item name
                if item in self.ungrabbed_items:
                    self.ungrabbed_items.remove(item)
                    self.inventory.append(item)
                    self.update_output(f'<span style="color:black;">User grabbed {item}.</span><br>')

                    # Automatically display the item after grabbing
                    if item == 'oobi pic':
                        self.show_image('./oobi.png')
                    elif item == 'chill':
                        self.show_image('./chill.png')
                elif item in self.inventory:
                    self.update_output(f'<span style="color:black;">{item} is already in your inventory!</span><br>')
                else:
                    self.update_output(f'<span style="color:black;">There is no item {item} to grab.</span><br>')
            return

        # Handle 'list items' command
        if command == 'list' and len(parts) == 2 and parts[1].lower() == 'items':
            if self.inventory:
                items = ', '.join(self.inventory)
                self.update_output(f'<span style="color:black;">Items in your inventory: {items}</span><br>')
            else:
                self.update_output('<span style="color:black;">Your inventory is empty.</span><br>')
            return
        elif command == 'list':
            self.update_output(f'<span style="color:black;">{user_input} is not a valid command.</span><br>')
            return

        # Handle 'show' command
        if command == 'show':
            if len(parts) < 2:
                self.update_output('<span style="color:black;">An item must follow the command \'show\'.</span><br>')
            else:
                item = " ".join(parts[1:])  # Combine remaining parts into the item name
                if item in self.inventory:
                    self.update_output(f'<span style="color:black;">Showing {item}.</span><br>')
                    if item == 'oobi pic':
                        self.show_image('./oobi.png')  # Show oobi image
                    elif item == 'chill':
                        self.show_image('./chill.png')  # Show chill image
                else:
                    self.update_output(f'<span style="color:black;">You do not have {item} in your inventory.</span><br>')

    def show_image(self, image_path):
        # Create a resizable window with a QLabel for displaying the image
        self.image_window = QWidget()
        self.image_window.setWindowTitle("Image Display")

        layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Load the image
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Set initial scaled pixmap to fit within a maximum size, keeping aspect ratio
            scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

            # Enable QLabel scaling to let the image resize with the window
            self.image_label.setScaledContents(True)
            
            layout.addWidget(self.image_label)
            self.image_window.setLayout(layout)
            
            # Set a reasonable initial window size and make the window resizable
            self.image_window.resize(400, 400)
            self.image_window.show()
        else:
            # If image is not found or loading fails
            self.update_output("<span style='color:black;'>Image not found!</span><br>")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = AdventureGame()
    game.show()
    sys.exit(app.exec_())
