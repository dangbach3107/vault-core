"""Generate synthetic browser-test documents under ignored .tmp/fixtures."""
from PIL import Image, ImageDraw
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from backend.app.core.config import REPOSITORY_ROOT


def main():
    root = REPOSITORY_ROOT / ".tmp" / "fixtures"
    root.mkdir(parents=True, exist_ok=True)
    for number, color in [(1, "#244d36"), (2, "#285d81")]:
        picture = Image.new("RGB", (800, 450), "#f4f5f0")
        draw = ImageDraw.Draw(picture)
        draw.rectangle((30, 30, 770, 420), outline=color, width=4)
        draw.text((70, 100), f"VAULT / SYNTHETIC DOCUMENT / VERSION {number}", fill=color, font_size=24)
        draw.text((70, 180), "For local upload and version-history testing only.", fill=color, font_size=20)
        picture.save(root / f"sample-v{number}.png")
    writer = PdfWriter()
    page = writer.add_blank_page(width=595, height=842)
    page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})})})
    stream = DecodedStreamObject()
    stream.set_data(b"BT /F1 20 Tf 60 740 Td (VAULT - SYNTHETIC PDF) Tj 0 -40 Td /F1 12 Tf (Local preview test. No real company data.) Tj ET")
    page[NameObject("/Contents")] = writer._add_object(stream)
    second = writer.add_blank_page(width=595, height=842)
    second[NameObject("/Resources")] = page["/Resources"]
    second_stream = DecodedStreamObject()
    second_stream.set_data(b"BT /F1 20 Tf 60 740 Td (SECOND SYNTHETIC PAGE) Tj ET")
    second[NameObject("/Contents")] = writer._add_object(second_stream)
    writer.write(root / "sample.pdf")
    print("Created synthetic PDF and PNG fixtures under .tmp/fixtures.")


if __name__ == "__main__":
    main()
