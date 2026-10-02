# kavel-haystack

A [Haystack](https://haystack.deepset.ai) component that generates and edits images with
[Kavel AI](https://www.kavel.ai/?utm_source=haystack&utm_medium=package), with **no API key needed** to start.

```bash
pip install kavel-haystack
```

```python
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from kavel_haystack import KavelImageGenerator

pipe = Pipeline()
pipe.add_component("prompt", PromptBuilder(template="A cover image for an article about {{topic}}, editorial photo, soft light"))
pipe.add_component("image", KavelImageGenerator(aspect_ratio="16:9"))
pipe.connect("prompt.prompt", "image.prompt")

pipe.run({"prompt": {"topic": "sourdough baking"}})["image"]["images"]
# ['https://cdn.kavel.ai/uploads/kie/image/....webp']
```

Without a key it runs on Kavel's free anonymous tier. On 2026-10-02 a fresh client id was granted
5 credits and one generated image spent all five; free output is 1K and watermarked. Set
`KAVEL_API_KEY` (or pass `api_key=Secret.from_token(...)`) with a key from
[kavel.ai/settings/apikeys](https://www.kavel.ai/settings/apikeys?utm_source=haystack&utm_medium=package)
to run on your account, edit images with `image_url=`, and pick a model with `model=`.

MIT licensed.
