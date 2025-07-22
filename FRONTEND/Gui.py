import os
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # suppress INFO and WARNING logs

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout, 
    QLabel, QHBoxLayout, QPushButton, QFrame, QSizePolicy, QSplitter
)
from PyQt5.QtGui import QIcon, QColor, QFont, QPixmap, QTextCharFormat, QTextBlockFormat, QMovie
from PyQt5.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "SOUL AI")  # Default name
current_dir = os.getcwd()
Old_chat_message = ""
TempDirPath = f"{current_dir}/Frontend/Files"
GraphicsDirPath = f"{current_dir}/Frontend/Graphics"


# Ensure directories exist
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

# Utility Functions
def AnswerModifier(answer):
    """Clean up response formatting"""
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def QueryModifier(query):
    """Normalize user queries"""
    new_query = query.lower().strip()
    if not new_query:
        return ""
        
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", 
                     "which", "whose", "whom", "can you", "what's", 
                     "where's", "how's"]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] not in ['?', '.', '!']:
            new_query += "?"
    else:
        if query_words[-1][-1] not in ['?', '.', '!']:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(command):
    """Set microphone status in file"""
    with open(os.path.join(TempDirPath, "Mic.data"), "w", encoding="utf-8") as file:
        file.write(command)

def GetMicrophoneStatus():
    """Get current microphone status"""
    try:
        with open(os.path.join(TempDirPath, "Mic.data"), "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "True"  # Default to active

def SetAssistantStatus(status):
    """Set assistant status message"""
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(status)

def GetAssistantStatus():
    """Get current assistant status"""
    try:
        with open(os.path.join(TempDirPath, "Status.data"), "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Ready"

def ShowTextToScreen(text):
    """Display text in the chat interface"""
    with open(os.path.join(TempDirPath, "Response.data"), "w", encoding="utf-8") as file:
        file.write(text)

def GraphicsDirectoryPath(filename):
    """Get full path to graphics file"""
    return os.path.join(GraphicsDirPath, filename)

def MicButtonInitiated():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")  

def TempDirectoryPath(filename):
    return os.path.join("C:/Users/KHUSHBOO/OneDrive/Desktop/SOUL/FRONTEND/Files", filename)

# def TempDirectoryPath(filename):
#     """Get full path to temp file"""
#     return os.path.join(TempDirPath, filename)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)

        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)  # No text interaction
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(0, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        movie = QMovie(GraphicsDirectoryPath("AIA2.gif"))
        max_gif_size_W = 300
        max_gif_size_H = 300
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        self.label = QLabel()
        self.label.setStyleSheet("color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        layout.setSpacing(10)
        layout.addWidget(self.gif_label)

        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_messages)
        self.timer.timeout.connect(self.SpeechRecognText)
        self.timer.start(5)
   #-------------------------------------------------------------
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                    QScrollBar:vertical {
                        border: none;
                        background: black;
                        width: 10px;
                        margin: 0px 0px 0px 0px;
                    }
                    
                    QScrollBar::handle:vertical {
                    background: white;
                    min-height: 20px;
                    }

                    QScrollBar::add-line:vertical {
                        background: black;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                        height: 10px;
                    }

                    QScrollBar::sub-line:vertical {
                        background: black;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                        height: 10px;               
                    }
                                    
                    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
                        border: none;
                        background: none;
                        color:none;
                        }
                    QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
                        background:none;
                                    }                                               
            """)  
        


    def typeNextWord(self):
        if self.typing_index < len(self.typed_message):
            cursor = self.chat_text_edit.textCursor()
            cursor.movePosition(cursor.End)  # Always type at the end
            cursor.insertText(self.typed_message[self.typing_index])
            self.typing_index += 1
            self.chat_text_edit.setTextCursor(cursor)
        else:
            self.typing_timer.stop()

#remember line 206 this is extra-------------------------------------------
    def load_messages(self):
         global Old_chat_message
         try:
             with open(TempDirectoryPath('Response.data'), "r", encoding="utf-8") as file:
                 messages = file.read()
         except FileNotFoundError:
             messages = ""  # or whatever default you want

         if not messages:
             return
         if str(Old_chat_message) == str(messages):
             return
         else:
             self.addMessage(message=messages, color="White")
             Old_chat_message = messages

                 # Append a newline before new message for separation
   
    
    #def SpeechRecognText(self):
        #with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            #messages = file.read()
            #self.label.setText(messages)
    def SpeechRecognText(self):
        try:
            with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
                messages = file.read()
                self.label.setText(messages)
        except PermissionError:
            print("⚠️ Permission denied when trying to read Status.data")
            self.label.setText("Unable to read status — permission denied.")
        except FileNotFoundError:
            print("⚠️ File not found: Status.data")
            self.label.setText("Status file not found.")		

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("mic_on.png"), 60, 60) #should edit
            MicButtonInitiated()
        else:
            self.load_icon(GraphicsDirectoryPath("mic_off.png"), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)


class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # 👉 Define a square size based on screen dimensions
        #square_size = int(min(screen_width, screen_height) * 0.4) 
        square_size = 860
 # You can adjust the 0.4 scale factor

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("SOUL")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: white;
            font-size: 50px;
            font-weight: bold;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            margin-top: 10px;
            margin-bottom: 0px;                      
        """)

        content_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        content_layout.setSpacing(0)  # or even 0 for tighter packing

        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("AIA.gif"))

        # 👉 Scale the movie to a square size
        movie.setScaledSize(QSize(square_size, square_size))

        gif_label.setMovie(movie)
        gif_label.setFixedSize(square_size, square_size)  # Ensure the label itself is also square
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Prevent automatic stretching

        movie.start()

        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath("mic_on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.toggled = False
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")

        # Add widgets to layout
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)


# class InitialScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(0, 0, 0, 0)
#         gif_label = QLabel()
#         movie = QMovie(GraphicsDirectoryPath("AIA.gif"))
#         gif_label.setMovie(movie)
#         max_gif_size_H = int(screen_width / 16 * 9)
#         movie.setScaledSize(QSize(screen_width, max_gif_size_H))
#         gif_label.setAlignment(Qt.AlignCenter)
#         movie.start()
#         gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.icon_label = QLabel()
#         pixmap = QPixmap(GraphicsDirectoryPath("mic_on.png"))
#         new_pixmap = pixmap.scaled(60, 60)
#         self.icon_label.setPixmap(new_pixmap)
#         self.icon_label.setFixedSize(150, 150)
#         self.icon_label.setAlignment(Qt.AlignCenter)
#         self.toggled = True
#         self.toggle_icon()
#         self.icon_label.mousePressEvent = self.toggle_icon
#         self.label = QLabel("")
#         self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
#         content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
#         content_layout.setContentsMargins(0, 0, 0, 150)
#         self.setLayout(content_layout)
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)
#         self.setStyleSheet("background-color: black;")
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath('Status.data'), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("mic_on.png"), 60, 60)
            MicButtonInitiated()
        else:
            self.load_icon(GraphicsDirectoryPath("mic_off.png"), 60, 60)
            MicButtonClosed()

            self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        home_button = QPushButton()
        # Additional UI elements like icons, buttons etc. likely follow...
        home_icon = QIcon(GraphicsDirectoryPath("home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("   Home")
        
        home_button.setStyleSheet("height:40px; line-height:40px; background-color:white ; color: black")

        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("   Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white ; color: black")

        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath("minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet('background-color:white')
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath('close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet('background-color:white')
        close_button.clicked.connect(self.closeWindow)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")
        title_label = QLabel(f" {str(Assistantname).capitalize()}")
        title_label.setStyleSheet("color: black; font-size:18px; background-color:white;")
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None

    def paintEvent(self,event):
        painter=QPainter(self)
        painter.fillRect(self.rect(),Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
      self.parent().showMinimized()

    def maximizeWindow(self):
        window = self.window()
        if window.isMaximized():
            window.showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            window.showMaximized()
            self.maximize_button.setIcon(self.restore_icon)
        self.maximize_button.repaint()  # Force refresh of the icon

    # def maximizeWindow(self):
    #     if self.parent().isMaximized():
    #         self.parent().showNormal()
    #         self.maximize_button.setIcon(self.maximize_icon)
    #     else:
    #         self.parent().showMaximized()
    #         self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
      self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen

class MainWindow(QMainWindow):
      def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

      def initUI(self):
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()
            stacked_widget = QStackedWidget(self)
            initial_screen = InitialScreen()
            message_screen = MessageScreen()
            stacked_widget.addWidget(initial_screen)
            stacked_widget.addWidget(message_screen)
            self.setGeometry(0, 0, screen_width, screen_height)
            self.setStyleSheet("background-color: black;")
            top_bar = CustomTopBar(self, stacked_widget)
            self.setMenuWidget(top_bar)
            self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
   GraphicalUserInterface()





