from linebot import LineBotApi
from linebot.models import ( RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction )

line_bot_api = LineBotApi ( 'CaHu+Fjeg5/1,62' )

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=800,height=270),
    selected=False,
    name="Richmenu",
    chat_bar_text="🔎 開 始 搜 尋 🔍",
    areas=[
        RichMenuArea(
            # (0,0)到(800,270)都是可點擊範圍
            bounds=RichMenuBounds(x=0, y=0, width=800, height=270),
            action=MessageAction(label='開始查詢',text='開始查詢')
        )
    ]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)


with open("C://Users//menu.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
    
print(rich_menu_id)
