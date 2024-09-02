from controller import (
    web,
    db,
    send,
    browser,
)

routers = [
    web.router,
    db.router,
    send.router,
    browser.router,
]
