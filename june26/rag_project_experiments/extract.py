"""
Extract text, embedded images and vector diagrams from a PDF.

Output:

knowledge/
└── book/
    └── extracted/
        ├── text/
        │   ├── page_1.txt
        │   ├── page_2.txt
        │   └── ...
        └── images/
            ├── page_1_img_1.png
            ├── page_2_vector_1.png
            ├── page_2_vector_2.png
            └── ...
"""

import os
import fitz  # PyMuPDF

KNOWLDEDGE_DIR = "./knowledge/book"


def merge_rectangles(rects, distance=20):
    """
    Merge nearby rectangles into larger regions.
    Useful for grouping vector drawings into a single diagram.
    """

    merged = []

    for rect in rects:

        found = False

        for i, m in enumerate(merged):

            expanded = fitz.Rect(
                m.x0 - distance,
                m.y0 - distance,
                m.x1 + distance,
                m.y1 + distance,
            )

            if expanded.intersects(rect):

                m.include_rect(rect)
                merged[i] = m
                found = True
                break

        if not found:
            merged.append(fitz.Rect(rect))

    return merged


def extract(book_path="./knowledge/book/chaper1.pdf"):

    text_dir = os.path.join(KNOWLDEDGE_DIR, "extracted", "text")
    image_dir = os.path.join(KNOWLDEDGE_DIR, "extracted", "images")

    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    doc = fitz.open(book_path)

    print(f"Processing {book_path}")
    print(f"Pages : {len(doc)}")

    for page_index, page in enumerate(doc):

        page_num = page_index + 1

        print(f"\nPage {page_num}")

        ###############################################################
        # TEXT
        ###############################################################

        text = page.get_text("text")

        with open(
            os.path.join(text_dir, f"page_{page_num}.txt"),
            "w",
            encoding="utf-8",
        ) as fp:
            fp.write(text)

        ###############################################################
        # EMBEDDED IMAGES
        ###############################################################

        image_list = page.get_images(full=True)

        print(f"Embedded Images : {len(image_list)}")

        for img_index, img in enumerate(image_list, start=1):

            xref = img[0]

            base = doc.extract_image(xref)

            with open(
                os.path.join(
                    image_dir,
                    f"page_{page_num}_img_{img_index}.{base['ext']}",
                ),
                "wb",
            ) as fp:
                fp.write(base["image"])

        ###############################################################
        # VECTOR DIAGRAMS
        ###############################################################

        drawings = page.get_drawings()

        print(f"Vector Drawings : {len(drawings)}")

        rects = []

        for drawing in drawings:

            r = drawing["rect"]

            #
            # Ignore tiny objects like letters, dots etc.
            #
            if r.width < 40:
                continue

            if r.height < 40:
                continue

            rects.append(r)

        merged = merge_rectangles(rects)

        print(f"Detected Diagram Regions : {len(merged)}")

        vector_index = 1

        for rect in merged:

            #
            # Ignore tiny merged regions
            #
            if rect.width < 120:
                continue

            if rect.height < 120:
                continue

            #
            # Small margin
            #
            clip = fitz.Rect(
                rect.x0 - 10,
                rect.y0 - 10,
                rect.x1 + 10,
                rect.y1 + 10,
            )

            pix = page.get_pixmap(
                clip=clip,
                dpi=300,
                alpha=False,
            )

            pix.save(
                os.path.join(
                    image_dir,
                    f"page_{page_num}_vector_{vector_index}.png",
                )
            )

            vector_index += 1


if __name__ == "__main__":
    extract()