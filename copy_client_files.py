import os
import shutil

def copy_client_files():
    """Copiando arquivo do client pro diretório de dist"""
    
    source_dir = "sistema-despesas-client"
    dest_dir = "dist"
    
    files_to_copy = [
        "index.html",
        "styles.css", 
        "scripts.js"
    ]
    
    img_dest = os.path.join(dest_dir, "img")
    if not os.path.exists(img_dest):
        os.makedirs(img_dest)
    
    for file in files_to_copy:
        src = os.path.join(source_dir, file)
        dst = os.path.join(dest_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ Copied: {file}")
        else:
            print(f"❌ File not found: {src}")
    
    img_src = os.path.join(source_dir, "img", "money.png")
    img_dst = os.path.join(img_dest, "money.png")
    if os.path.exists(img_src):
        shutil.copy2(img_src, img_dst)
        print("✅ Copied: img/money.png")
    else:
        print(f"❌ Image not found: {img_src}")

if __name__ == "__main__":
    copy_client_files() 