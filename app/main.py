from fastapi import FastAPI
from app.database import engine, Base
from app.models import user

# 1. YENİ EKLENDİ: Yazdığımız router'ı içeri aktarıyoruz
from app.routers import product, user, auth, category, cart, cartItem

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Ticaret API",
    description="Docker ve FastAPI ile E-ticaret Projesi",
    version="1.0.0"
)

# 2. YENİ EKLENDİ: Router'ı ana uygulamamıza bağlıyoruz
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(cart.router)
app.include_router(cartItem.router)

@app.get("/")
def read_root():
    return {"mesaj": "Sistem aktif! Veritabanı tabloları başarıyla oluşturuldu."}