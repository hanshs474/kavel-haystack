"""Kavel image generation as a Haystack component.

Without an API key the component uses Kavel's free anonymous tier, so a
pipeline runs on a machine with nothing configured. Pass ``api_key`` (a
Haystack ``Secret``) or set ``KAVEL_API_KEY`` to run on a kavel.ai account.
"""

from typing import Any, Dict, List, Optional

import kavel
from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace


@component
class KavelImageGenerator:
    """Generates an image from a prompt, or edits one, and returns its URL.

    Usage:
        ```python
        from kavel_haystack import KavelImageGenerator

        gen = KavelImageGenerator(aspect_ratio="16:9")
        result = gen.run(prompt="a paper boat at sunrise, soft fog, 35mm film")
        result["images"]  # ["https://cdn.kavel.ai/..."]
        ```
    """

    def __init__(
        self,
        aspect_ratio: str = "1:1",
        api_key: Secret = Secret.from_env_var("KAVEL_API_KEY", strict=False),
        model: Optional[str] = None,
        timeout: float = 360.0,
    ):
        self.aspect_ratio = aspect_ratio
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(
            self, aspect_ratio=self.aspect_ratio, api_key=self.api_key.to_dict(),
            model=self.model, timeout=self.timeout,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KavelImageGenerator":
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    @component.output_types(images=List[str])
    def run(self, prompt: str, image_url: Optional[str] = None) -> Dict[str, List[str]]:
        """Generate one image, or edit the image at ``image_url`` (editing needs an API key).

        Raises ``kavel.QuotaError`` when the free allowance is spent and
        ``kavel.RejectedError`` when the prompt is refused.
        """
        url = kavel.generate(
            prompt,
            image_url=image_url,
            aspect_ratio=self.aspect_ratio,
            api_key=self.api_key.resolve_value(),
            model=self.model,
            timeout=self.timeout,
        )
        return {"images": [url]}
