import pygame as pg

import thehand as th


class RpsScene(th.Scene):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
    ) -> None:
        super().__init__(state, store, name)

        self.machine_background = pg.Surface((self.state.window_size[0], int(self.state.window_size[1] * 0.5)))
        self.machine_background.fill(th.COLOR_MOCHA_RED)

        self.player_imgs = {
            "rock": self.store.imgs["rock"].convert_alpha(),
            "paper": self.store.imgs["paper"].convert_alpha(),
            "scissor": self.store.imgs["scissor"].convert_alpha(),
        }
        self.machine_imgs = {
            "rock": pg.transform.rotate(self.player_imgs["rock"], 180),
            "paper": pg.transform.rotate(self.player_imgs["paper"], 180),
            "scissor": pg.transform.rotate(self.player_imgs["scissor"], 180),
        }

        self.player_hand = self.player_imgs["rock"]
        self.player_hand_rect = self.player_hand.get_rect(
            center=(
                int(self.state.window_size[0] * 0.9),
                int(self.state.window_size[1] * 0.8),
            )
        )
        self.second_player_hand = self.player_imgs["paper"]
        self.second_player_hand_rect = self.second_player_hand.get_rect(
            center=(
                int(self.state.window_size[0] * 0.6),
                int(self.state.window_size[1] * 0.9),
            )
        )

        self.machine_hand = self.player_imgs["rock"]
        self.machine_hand_rect = self.machine_hand.get_rect(
            center=(
                int(self.state.window_size[0] * 0.1),
                int(self.state.window_size[1] * 0.2),
            )
        )
        self.machine_hand = pg.transform.rotate(self.machine_hand, 180)

        self._last_gesture = ""
        self._second_hand = False
        self._second_hand_timer = 0

        self.shocked_buffer = None
        self.loading_buffer = None
        self.error_buffer = None

    def setup(self) -> None:
        self.state.set_scene_hand_callback(self._hand_callback)
        self.state.hand_running = True

    def handle_events(self) -> None:
        return

    def update(self) -> None:
        if self._second_hand:
            self.state.hand_running = False
            if not self.error_buffer:
                self.error_buffer = self.store.sounds["windows_error_remix"].play()
            else:
                if not self.error_buffer.get_busy():
                    pg.event.post(th.create_next_scene_event())
            if not self.loading_buffer or not self.loading_buffer.get_busy():
                self.loading_buffer = self.store.sounds["loading"].play()

    def render(self) -> None:
        screen = self.store.screen
        screen.fill(th.COLOR_MOCHA_BLUE)

        screen.blit(self.machine_background, (0, 0))

        screen.blit(self.player_hand, self.player_hand_rect)
        screen.blit(self.machine_hand, self.machine_hand_rect)

        if self._second_hand:
            screen.blit(self.second_player_hand, self.second_player_hand_rect)

            board_size = (self.state.window_size[0] * 0.65, self.state.window_size[1] / 2)
            board = pg.Surface(board_size, pg.SRCALPHA)
            board.fill((0, 0, 0, 178))

            image = self.store.imgs["fair_icon"].convert_alpha()
            image = pg.transform.scale(image, (board_size[1] * 0.7, board_size[1] * 0.7))
            image_rect = image.get_rect(center=(board_size[0] / 2, board_size[1] / 2 - 50))
            board.blit(image, image_rect)

            font = self.store.font_pixel_36
            text = font.render("Congratulations, fair win!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(board_size[0] / 2, board_size[1] / 2 + 100))
            board.blit(text, text_rect)

            board_rect = board.get_rect(center=(self.state.window_size[0] / 2, self.state.window_size[1] / 2))
            self.store.screen.blit(board, board_rect)

    def _hand_callback(self, result: th.HandLandmarkerResult):
        if not result.hand_world_landmarks:
            return

        meet_rock = False
        meet_paper = False
        meet_scissor = False

        for landmarks in result.hand_world_landmarks:
            if len(landmarks) < 21:
                return

            meet_rock = max(meet_rock, th.is_hand_punch(landmarks))
            meet_paper = max(meet_paper, th.is_hand_palm(landmarks))
            meet_scissor = max(meet_scissor, th.is_hand_v(landmarks))

        if sum([meet_rock, meet_paper, meet_scissor]) >= 2:
            self._second_hand = True
            self._second_hand_timer = self.state.now
            if meet_rock and meet_paper:
                self.player_hand = self.player_imgs["rock"]
                self.second_player_hand = self.player_imgs["paper"]
                self.machine_hand = self.machine_imgs["scissor"]
            elif meet_paper and meet_scissor:
                self.player_hand = self.player_imgs["paper"]
                self.second_player_hand = self.player_imgs["scissor"]
                self.machine_hand = self.machine_imgs["rock"]
            elif meet_scissor and meet_rock:
                self.player_hand = self.player_imgs["scissor"]
                self.second_player_hand = self.player_imgs["rock"]
                self.machine_hand = self.machine_imgs["paper"]
            return

        self._second_hand = False

        if meet_rock:
            if self._last_gesture != "rock":
                self.shocked_buffer = self.store.sounds["shocked"].play()
            self._last_gesture = "rock"
            self.player_hand = self.player_imgs["rock"]
            self.machine_hand = self.machine_imgs["paper"]
            return

        if meet_paper:
            if self._last_gesture != "paper":
                self.shocked_buffer = self.store.sounds["shocked"].play()
            self._last_gesture = "paper"
            self.player_hand = self.player_imgs["paper"]
            self.machine_hand = self.machine_imgs["scissor"]
            return

        if meet_scissor:
            if self._last_gesture != "scissor":
                self.shocked_buffer = self.store.sounds["shocked"].play()
            self._last_gesture = "scissor"
            self.player_hand = self.player_imgs["scissor"]
            self.machine_hand = self.machine_imgs["rock"]
            return
