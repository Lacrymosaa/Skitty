import sys
import getpass
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

class CalculatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        user = getpass.getuser()
        self.setWindowTitle(f"Skitty de {user}")
        self.setFixedSize(400, 500)

        # Definir o ícone da janela
        icon = QIcon("imgs/skitty.ico")  # Substitua pelo caminho do arquivo do ícone desejado
        self.setWindowIcon(icon)
        
        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Display da calculadora
        self.display = QLineEdit()
        self.display.setFixedHeight(60)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)  # Definir como somente leitura
        # Folha de estilo CSS para o QLineEdit do display
        display_style = '''
            QLineEdit {
                font-size: 24px;
                border: 5px solid lightpink;
                background-color: white;
            }
        '''
        self.display.setStyleSheet(display_style)
        main_layout.addWidget(self.display)
        
        # Layout dos botões
        button_layout = QGridLayout()
        main_layout.addLayout(button_layout)
        
        # Lista de botões e seus textos correspondentes
        buttons = [
            ('%', 'imgs/percent.png', 'percent'),
            ('CE', 'imgs/CE.png', 'CE'),
            ('C', 'imgs/clear.png', 'C'),
            ('⌫', 'imgs/del.png', 'del'),
            ('1/x', 'imgs/perone.png', 'perone'),
            ('x²', 'imgs/square.png', 'elevate'),
            ('√', 'imgs/root.png', 'root'),
            ('÷', 'imgs/divide.png', 'divide'),
            ('7', 'imgs/number.png', 'kitty'),
            ('8', 'imgs/number.png', 'kitty'),
            ('9', 'imgs/number.png', 'kitty'),
            ('*', 'imgs/multiply.png', 'multiply'),
            ('4', 'imgs/number.png', 'kitty'),
            ('5', 'imgs/number.png', 'kitty'),
            ('6', 'imgs/number.png', 'kitty'),
            ('-', 'imgs/multiply.png', 'minus'),
            ('1', 'imgs/number.png', 'kitty'),
            ('2', 'imgs/number.png', 'kitty'),
            ('3', 'imgs/number.png', 'kitty'),
            ('+', 'imgs/multiply.png', 'plus'),
            ('±', 'imgs/multiply.png', 'negate'),
            ('0', 'imgs/number.png', 'kitty'),
            ('.', 'imgs/multiply.png', 'dot'),
            ('=', 'imgs/multiply.png', 'equal'),
        ]

        # Folha de estilo CSS
        button_style = '''
            QPushButton {
                border: 3px groove rgba(0, 0, 0, 0.1);
                color: black;
                font-size: 20px;
                height: 45px;
                width: 60px;
            }

            QPushButton.kitty {
                background-color: #E29FA6;
            }

            QPushButton.percent {
                background-color: #B1D4E6;
            }

            QPushButton.CE {
                background-color: #e9cedc;
            }

            QPushButton.C {
                background-color: #CEBAD0;
            }

            QPushButton.del {
                background-color: #B0B0B2;
            }

            QPushButton.perone {
                background-color: #A7CED0;
            }

            QPushButton.elevate {
                background-color: #BEC8F9;
            }

            QPushButton.root {
                background-color: #EBCD63;
            }

            QPushButton.divide {
                background-color: #A9BE61;
            }

            QPushButton.multiply {
                background-color: #FFFFFF;
            }

            QPushButton.minus {
                background-color: #FFFFFF;
            }
            
            QPushButton.plus {
                background-color: #FFFFFF;
            } 

            QPushButton.negate {
                background-color: #FFFFFF;
            } 

            QPushButton.dot {
                background-color: #FFFFFF;
            } 

            QPushButton.equal {
                background-color: #FFFFFF;
            } 

            QPushButton:hover {
                border: 3px groove rgba(0, 0, 0, 0.25);
            }
            
            QPushButton:pressed {
                border: 3px groove rgba(0, 0, 0, 0.32);
            }
        '''
        
        # Adicionar botões ao layout
        row, col = 0, 0
        for btn_text, btn_image, btn_class in buttons:
            button = QPushButton(btn_text)
            button.setIcon(QIcon(btn_image))
            button.setIconSize(button.sizeHint())
            button.clicked.connect(lambda ch, text=btn_text: self.handle_button(text))
            button.setStyleSheet(button_style)
            button.setProperty('class', btn_class)
            button_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Criar um QMovie a partir do GIF animado convertido em sequência de imagens PNG
        movie = QMovie("imgs/glitter.gif")  # Substitua pelo caminho do arquivo GIF convertido em PNG
        movie.setScaledSize(self.size())  # Definir o tamanho do GIF animado como o tamanho da janela
        movie.setCacheMode(QMovie.CacheAll)  # Cachear todas as imagens para um desempenho mais suave
        movie.setSpeed(100)  # Definir a velocidade do GIF animado (opcional)

        # Criar um QLabel para exibir o QMovie como plano de fundo
        background_label = QLabel(self)
        background_label.setMovie(movie)
        background_label.setGeometry(self.rect())  # Definir a geometria do QLabel para cobrir toda a janela
        background_label.lower()  # Colocar o QLabel no fundo para servir como plano de fundo

        # Iniciar a reprodução do QMovie
        movie.start()
    
    def handle_button(self, text):
        current_text = self.display.text()
        if current_text == '0':
            self.display.setText(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.display.clear()
        elif text == '⌫':
            self.display.backspace()
        elif text == '√':
            self.display.setText('sqrt(' + self.display.text() + ')')
        elif text == '÷':
            self.display.setText(self.display.text() + '/')
        elif text == 'x²':
            self.display.setText(self.display.text() + '**2')
        elif text == '1/x':
            self.display.setText('1/' + self.display.text())
        elif text == '±':
            self.display.setText('-' + self.display.text())
        elif text == 'CE':
            self.display.setText('')
        elif text == '%':
            expression = self.display.text()
            try:
                result = eval(expression) / 100
                self.display.setText(str(result))
            except Exception as e:
                print(f"Erro de cálculo: {e}")
        else:
            self.display.setText(self.display.text() + text)

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.handle_button('=')
        elif key == Qt.Key_Z:
            self.display.backspace()
        elif key == Qt.Key_Period:
            self.handle_button('.')
        elif key == Qt.Key_Plus:
            self.handle_button('+')
        elif key == Qt.Key_Minus:
            self.handle_button('-')
        elif key == Qt.Key_Asterisk:
            self.handle_button('*')
        elif key == Qt.Key_Slash:
            self.handle_button('÷')
        elif key == Qt.Key_Percent:
            self.handle_button('%')
        elif key == Qt.Key_0:
            self.handle_button('0')
        elif key == Qt.Key_1:
            self.handle_button('1')
        elif key == Qt.Key_2:
            self.handle_button('2')
        elif key == Qt.Key_3:
            self.handle_button('3')
        elif key == Qt.Key_4:
            self.handle_button('4')
        elif key == Qt.Key_5:
            self.handle_button('5')
        elif key == Qt.Key_6:
            self.handle_button('6')
        elif key == Qt.Key_7:
            self.handle_button('7')
        elif key == Qt.Key_8:
            self.handle_button('8')
        elif key == Qt.Key_9:
            self.handle_button('9')
        elif key == Qt.Key_C:
            self.handle_button('C')

    def calculate(self):
        try:
            expression = self.display.text()
            expr = parse_expr(expression)
            result = expr.evalf()
            result = str(result).rstrip('0').rstrip('.')  # Remove os zeros desnecessários
            self.display.setText(str(result))
        except Exception as e:
            print(f"Erro de cálculo: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec_())
