window_stylesheet = ("""
    QWidget {
        background-color: #f0f0f0;  /* Light background for the entire window */
        font-family: Arial, Helvetica, sans-serif;
    }
    QLabel {
        color: #333;  /* Dark text color for labels */
    }
    QPushButton {
        background-color: #4CAF50;  /* Green button background */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 18px;
    }
    QPushButton:hover {
        background-color: #45a049;  /* Slightly darker green on hover */
    }
    QPushButton:pressed {
        background-color: #3e8e41;  /* Even darker green when pressed */
    }
    QSpinBox {
        background-color: white; 
        border: 1px solid #ccc; 
        border-radius: 5px;
    }
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
    }
    QListWidget {
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    QToolBox::tab {
        background: #e7e7e7;
        border: 1px solid #ccc;
        padding: 5px;
        font-size: 18px;
    }
    QToolBox::tab:selected {
        background: #d6d6d6;
        font-weight: bold;
    }
""")

# =================================================================== #
# ====================== MAIN MENU STYLESHEETS ====================== #
# =================================================================== #

header_stylesheet = ("""
    font-size: 36px;
    font-weight: bold;
    color: #2c3e50;  /* A dark blue-gray color */
    margin: 20px 0;
    text-align: center;
""")

blue_button_stylesheet = ("""
QPushButton {
        background-color: #007BFF;  /* Blue background */
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #0056b3;  /* Darker blue on hover */
    }
    QPushButton:pressed {
        background-color: #004494;  /* Even darker blue when pressed */
    }
""")

orange_button_stylesheet = ("""
    QPushButton {
        background-color: #FF5722;  /* Orange background */
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #e64a19;  /* Darker orange on hover */
    }
    QPushButton:pressed {
        background-color: #d84315;  /* Even darker orange when pressed */
    }
""")

label_stylesheet = ("""
    QLabel {
        color: #333333;        /* Text color: dark gray */
        font-size: 18px;       /* Default font size for labels */
        font-weight: normal;   /* Default font weight */
        padding: 5px;          /* Padding for better spacing */
        margin: 0px;           /* Remove extra margin */
    }
    QLabel.title {
        font-size: 36px;       /* Larger font for title labels */
        font-weight: bold;     /* Bold for emphasis */
        color: #2c3e50;        /* Blue-gray color */
        margin-bottom: 20px;   /* Add space below title labels */
        text-align: center;
    }
    QLabel.highlight {
        font-size: 20px;       /* Slightly larger font for important labels */
        font-weight: bold;     /* Bold for emphasis */
        color: #007BFF;        /* Blue for highlights */
    }
    QLabel.error {
        font-size: 16px;       /* Slightly smaller font for error messages */
        color: #FF0000;        /* Red for errors */
        font-weight: bold;
    }
""")

# toolbox_stylesheet = ("""
#     QToolBox {
#         border: none;  /* Remove the default border */
#         background-color: #f9f9f9;  /* Light background */
#     }
#     QToolBox::tab {
#         background: #e0e0e0;  /* Light gray tab */
#         border: 1px solid #ccc;
#         padding: 8px;
#         font-size: 18px;
#         font-weight: bold;
#         text-align: left;
#     }
#     QToolBox::tab:selected {
#         background: #d0d0d0;  /* Slightly darker gray for selected tab */
#     }
# """)

toolbox_stylesheet = ("""
    QToolBox {
        background-color: #F9F9F9;      /* Light background for toolbox */
        border: 1px solid #D3D3D3;      /* Subtle border for the entire toolbox */
    }

    QToolBox::tab {
        background: #E0E0E0;            /* Background for tabs */
        border: 1px solid #B0B0B0;      /* Border around each tab */
        border-radius: 3px;             /* Rounded corners for a modern look */
        padding: 5px;                   /* Add padding inside tabs */
        margin: 2px;                    /* Space between tabs to avoid crowding */
        color: #333333;                 /* Text color */
        font-size: 16px;                /* Font size for tab text */
        font-weight: bold;              /* Bold text for tab labels */
    }

    QToolBox::tab:selected {
        background: #D0E8FF;            /* Highlighted background for the selected tab */
        border-color: #007BFF;          /* Blue border for active tab */
        color: #0056b3;                 /* Darker blue for selected text */
    }

    QListWidget {
        border: 1px solid #B0B0B0;      /* Add border to the list widget */
        background-color: #FFFFFF;     /* Clean white background */
        padding: 5px;                   /* Padding inside the list widget */
        font-size: 16px;                /* Font size for list items */
    }
""")

text_input_stylesheet = ("""
    QLineEdit {
        background-color: white;
        border: 2px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        font-size: 18px;
    }
    QLineEdit:focus {
        border-color: #007BFF;  /* Highlighted border when focused */
    }
""")

spinbox_stylesheet = ("""
    QSpinBox {
        background-color: white;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 18px;
        padding: 5px;
    }
    QSpinBox:focus {
        border-color: #007BFF;  /* Highlighted border when focused */
    }
""")

list_stylesheet = ("""
    QListWidget {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        font-size: 18px;
    }
    QListWidget::item {
        padding: 8px;
    }
    QListWidget::item:selected {
        background-color: #007BFF;  /* Highlight selected item */
        color: white;
    }
""")

divider_stylesheet = ("""
    QFrame {
        background-color: #ccc;  /* Light gray divider */
        width: 2px;
    }
""")

dark_theme_stylesheet = ("""
    QWidget {
        background-color: #2e2e2e;
        color: #f0f0f0;
        font-family: Arial, Helvetica, sans-serif;
    }
    QLabel, QLineEdit, QListWidget {
        background-color: #3e3e3e;
        border: 1px solid #5a5a5a;
    }
    QPushButton {
        background-color: #007BFF;
        color: white;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }
""")

# =================================================================== #
# ======================= GAMEPLAY STYLESHEETS ====================== #
# =================================================================== #
