import os
import threading
import flet as ft
from yt_dlp import YoutubeDL

class SnapListApp:
    def __init__(self):
        self.barra_progresso = None
        self.mensagem_aguarde = None

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Snap List - Baixador de YouTube"
        self.page.window.width = 600
        self.page.window.height = 700
        self.page.padding = 20
        self.page.window.resizable = False
        self.page.window.maximizable = False
        self.page.theme_mode = "dark"
        self.page.bgcolor = ft.Colors.BLACK
        self.page.icon = "log.png"

        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.logo = ft.Image(
            src="log.png",
            width=150,
            height=150,
            fit=ft.ImageFit.CONTAIN
        )

        self.campo_url = ft.TextField(
            label="Insira a URL do vídeo ou playlist",
            border_color=ft.Colors.WHITE,
            width=400,
            text_align=ft.TextAlign.CENTER,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)
        )

        self.botao_video = ft.ElevatedButton(
            text="Baixar Vídeo (MP4)",
            on_click=self.baixar_video,
            width=240,
            height=60,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE
        )

        self.botao_audio = ft.ElevatedButton(
            text="Baixar Áudio (MP3)",
            on_click=self.baixar_audio,
            width=240,
            height=60,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE
        )

        self.barra_progresso = ft.ProgressBar(
            width=400,
            value=0,
            color=ft.Colors.GREEN_400,
            bgcolor=ft.Colors.BLACK,
            visible=False
        )

        self.mensagem_aguarde = ft.Text(
            "",
            color=ft.Colors.YELLOW_200,
            size=14,
            text_align=ft.TextAlign.CENTER
        )

        conteudo_principal = ft.Container(
            content=ft.Column(
                [
                    self.logo,
                    ft.Container(
                        content=self.campo_url,
                        margin=ft.margin.only(bottom=20),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Row(
                            [self.botao_video, self.botao_audio],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        margin=ft.margin.only(bottom=20)
                    ),
                    ft.Container(
                        content=self.barra_progresso,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=self.mensagem_aguarde,
                        margin=ft.margin.only(top=10),
                        alignment=ft.alignment.center
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30,
            border_radius=10,
            bgcolor=ft.Colors.BLACK
        )

        self.page.add(conteudo_principal)

    def atualizar_barra_progresso(self, progresso):
        self.barra_progresso.value = progresso
        self.page.update()

    def mostrar_mensagem(self, mensagem):
        snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=ft.Colors.BLUE_GREY_900
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.page.update()

    def download(self, url, formato, extensao):
        pasta_destino = f"./downloads/{formato}"
        os.makedirs(pasta_destino, exist_ok=True)
        self.barra_progresso.visible = True
        self.atualizar_barra_progresso(0)
        self.mensagem_aguarde.value = "Aguarde, o download está em andamento..."
        self.page.update()

        try:
            ydl_opts = {
                'outtmpl': f'{pasta_destino}/%(playlist_index)s - %(title)s.{extensao}',
                'progress_hooks': [self.progress_hook],
                'noplaylist': False,
                'extract_flat': False,
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao baixar: {str(e)}")
        finally:
            self.barra_progresso.visible = False
            self.mensagem_aguarde.value = ""
            self.campo_url.value = ""
            self.atualizar_barra_progresso(0)
            self.page.update()

    def progress_hook(self, d):
        if d['status'] == 'finished':
            self.atualizar_barra_progresso(1)
            self.mostrar_mensagem("Download concluído!")
        elif d['status'] == 'downloading':
            if 'downloaded_bytes' in d and d['total_bytes'] is not None:
                progresso = d['downloaded_bytes'] / d['total_bytes']
                self.atualizar_barra_progresso(progresso)

    def baixar_video(self, e):
        url = self.campo_url.value
        if not url:
            self.mostrar_mensagem("Por favor, insira uma URL válida do YouTube.")
            return
        threading.Thread(target=self.download, args=(url, "videos", "mp4")).start()

    def baixar_audio(self, e):
        url = self.campo_url.value
        if not url:
            self.mostrar_mensagem("Por favor, insira uma URL válida do YouTube.")
            return
        threading.Thread(target=self.download, args=(url, "audios", "mp3")).start()

ft.app(target=SnapListApp().main)
