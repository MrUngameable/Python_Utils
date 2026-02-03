class ChatBubble(QFrame):
    def __init__(self, text, is_user=False, avatar_path=None):
        super().__init__()
        self.is_user = is_user
        self.text = text
        self.avatar_path = avatar_path

        self.setObjectName("ChatBubbleUser" if is_user else "ChatBubbleAI")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        #self.setLayout(self.layout)

        self._build_bubble()
        self._fade_in()

    def _build_bubble(self):
        # Clear layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Avatar
        avatar = self._build_avatar() if self.avatar_path else None
        self.text_view = self._build_text_view()

        if self.is_user:
            self.layout.addStretch()
            self.layout.addWidget(self.text_view)
            if avatar:
                self.layout.addWidget(avatar)
        
        else:
            if avatar:
                self.layout.addWidget(avatar)
            self.layout.addWidget(self.text_view)
            self.layout.addStretch()

    def _build_avatar(self):
        avatar = QLabel()
        pixmap = None

        # If avatar_path is a QIcon (from load_icon)
        if isinstance(self.avatar_path, QIcon):
            pixmap = self.avatar_path.pixmap(40, 40)
        
        # Else avatar_path is str / Path
        else:
            pixmap = QPixmap(str(self.avatar_path))
        
        if pixmap is None or pixmap.isNull():
            print("⚠️ Avatar Icon not found:", self.avatar_path)
        else:
            pixmap = pixmap.scaled(
                40, 40,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # Make circular mask
            mask = QPixmap(40, 40)
            mask.fill(Qt.transparent)
            painter = QPainter(mask)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(Qt.white)
            painter.drawEllipse(0, 0, 40, 40)
            painter.end()
            
            pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

            avatar.setPixmap(pixmap)
            avatar.setFixedSize(40, 40)

            # Glow ring effect
            glow = QGraphicsDropShadowEffect()
            glow.setBlurRadius(18)
            glow.setColor(QColor("#00d4ff"))
            glow.setOffset(0, 0)
            avatar.setGraphicsEffect(glow)

            return avatar
    
    def _build_text_view(self):
        view = QTextBrowser()
        view.setFrameShape(QFrame.NoFrame)
        view.setOpenExternalLinks(True)
        view.setReadOnly(True)
        view.setMaximumWidth(520)

        view.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.LinksAccessibleByMouse
        )

        view.setFont(QFont("Arial", 11))
        view.setContentsMargins(12, 8, 12, 8)
        view.setObjectName("ChatBubbleText")

        view.setMarkdown(self.text)
        return view
    
    def append_text(self, chunk: str):
        """
        Append streamed tokens safely.
        """
        self.text += chunk
        cursor = self.text_view.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(chunk)
        self.text_view.setTextCursor(cursor)

    def _fade_in(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(280)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()

        # keep reference
        self._fade_anim = anim