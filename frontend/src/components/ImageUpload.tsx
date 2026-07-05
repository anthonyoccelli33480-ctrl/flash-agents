import { useRef } from "react";

interface Props {
  images: string[];
  maxImages: number;
  onChange: (images: string[]) => void;
}

function readFile(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result as string);
    r.onerror = reject;
    r.readAsDataURL(file);
  });
}

export default function ImageUpload({ images, maxImages, onChange }: Props) {
  const ref = useRef<HTMLInputElement>(null);

  async function onFiles(files: FileList | null) {
    if (!files?.length) return;
    const next = [...images];
    for (const f of Array.from(files)) {
      if (!f.type.match(/^image\/(png|jpeg|jpg)$/)) continue;
      if (f.size > 4 * 1024 * 1024) continue;
      const data = await readFile(f);
      next.push(data);
      if (next.length >= maxImages) break;
    }
    onChange(next.slice(0, maxImages));
    if (ref.current) ref.current.value = "";
  }

  function remove(i: number) {
    onChange(images.filter((_, idx) => idx !== i));
  }

  return (
    <div className="image-upload">
      <div className="image-toolbar">
        <button type="button" className="img-btn" onClick={() => ref.current?.click()}>
          + Image {images.length > 0 ? `(${images.length}/${maxImages})` : `(PNG/JPEG, max ${maxImages})`}
        </button>
        <span className="img-hint">Gemma 4 31B — vision multimodale</span>
      </div>
      <input
        ref={ref}
        type="file"
        accept="image/png,image/jpeg,image/jpg"
        multiple={maxImages > 1}
        hidden
        onChange={(e) => onFiles(e.target.files)}
      />
      {images.length > 0 && (
        <div className="previews">
          {images.map((src, i) => (
            <div key={i} className="preview-wrap">
              <img src={src} alt={`upload-${i}`} className="preview" />
              <button type="button" className="remove" onClick={() => remove(i)} aria-label="Retirer">
                ×
              </button>
            </div>
          ))}
        </div>
      )}
      <style>{`
        .image-upload { margin-bottom: 1rem; }
        .image-toolbar { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 0.75rem; }
        .img-btn {
          padding: 0.5rem 1rem; border-radius: 8px; border: 1px dashed var(--accent);
          background: var(--accent-dim); color: var(--accent); font-weight: 600;
          cursor: pointer; font-size: 0.85rem;
        }
        .img-btn:hover { opacity: 0.9; }
        .img-hint { font-size: 0.75rem; color: var(--muted); font-family: var(--mono); }
        .previews { display: flex; gap: 0.75rem; flex-wrap: wrap; }
        .preview-wrap { position: relative; }
        .preview {
          max-height: 140px; max-width: 220px; border-radius: 8px;
          border: 1px solid var(--border); object-fit: contain; background: var(--bg);
        }
        .remove {
          position: absolute; top: 4px; right: 4px; width: 22px; height: 22px;
          border-radius: 50%; border: none; background: var(--red); color: #fff;
          cursor: pointer; font-size: 14px; line-height: 1;
        }
      `}</style>
    </div>
  );
}