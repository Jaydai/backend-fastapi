"""
Asset Fetcher Service

Handles fetching of external assets like organization logos and profile pictures.
Fetches from websites and LinkedIn profiles.
"""

import logging
import re
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

# HTTP client settings
HTTP_TIMEOUT = 10.0
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class AssetFetcherService:
    """
    Service for fetching external assets (logos, profile pictures).

    Features:
    - Fetch organization logos from websites
    - Fetch profile pictures from LinkedIn
    - Smart favicon detection with priority ordering
    - Fallback to common paths
    """

    def fetch_organization_logo(
        self,
        website_url: str | None = None,
        linkedin_url: str | None = None,
    ) -> str | None:
        """
        Fetch organization logo from website or LinkedIn.

        Args:
            website_url: Organization website URL
            linkedin_url: Organization LinkedIn URL

        Returns:
            Logo URL if found, None otherwise
        """
        logo_url = None

        # Try website first
        if website_url:
            logo_url = self._fetch_logo_from_website(website_url)

        # Try LinkedIn if no logo found
        if not logo_url and linkedin_url:
            logo_url = self._fetch_logo_from_linkedin(linkedin_url)

        return logo_url

    def fetch_profile_picture(
        self,
        linkedin_url: str | None = None,
    ) -> str | None:
        """
        Fetch profile picture from LinkedIn profile URL.

        Args:
            linkedin_url: User's LinkedIn profile URL

        Returns:
            URL of the profile picture or None if not found
        """
        if not linkedin_url:
            return None

        return self._fetch_picture_from_linkedin(linkedin_url)

    def _fetch_logo_from_website(self, website_url: str) -> str | None:
        """
        Fetch favicon/logo from website.

        Priority order:
        1. High-resolution favicon (icon with sizes attribute, prefer largest)
        2. Apple touch icon (usually high quality square icon)
        3. Standard favicon link
        4. /favicon.ico fallback
        5. og:image as last resort (often not a logo)
        """
        try:
            # Ensure URL has scheme
            if not website_url.startswith(("http://", "https://")):
                website_url = f"https://{website_url}"

            parsed = urlparse(website_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"

            with httpx.Client(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
                response = client.get(website_url)
                response.raise_for_status()
                html = response.text

                def resolve_url(url: str) -> str:
                    """Resolve relative URLs to absolute."""
                    if url.startswith("//"):
                        return f"https:{url}"
                    elif url.startswith("/"):
                        return base_url + url
                    elif not url.startswith(("http://", "https://")):
                        return f"{base_url}/{url}"
                    return url

                # 1. Look for high-res icons with sizes
                logo = self._find_sized_icon(html, resolve_url)
                if logo:
                    return logo

                # 2. Look for apple-touch-icon
                logo = self._find_apple_touch_icon(html, resolve_url)
                if logo:
                    return logo

                # 3. Look for any favicon link
                logo = self._find_favicon_link(html, resolve_url)
                if logo:
                    return logo

                # 4. Try common favicon paths
                logo = self._check_common_favicon_paths(client, base_url)
                if logo:
                    return logo

                # 5. og:image as last resort
                logo = self._find_og_image(html, resolve_url)
                if logo:
                    return logo

        except Exception as e:
            logger.warning(f"[ONBOARDING] Error fetching logo from website: {e}")

        return None

    def _find_sized_icon(
        self, html: str, resolve_url: callable
    ) -> str | None:
        """Find high-resolution icons with sizes attribute."""
        # Match: <link rel="icon" sizes="192x192" href="...">
        icon_with_sizes = re.findall(
            r'<link[^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*(?:sizes=["\'](\d+)x\d+["\'][^>]*)?href=["\']([^"\']+)["\']',
            html,
            re.IGNORECASE,
        )
        # Also match reversed attribute order
        icon_with_sizes += re.findall(
            r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:icon|shortcut icon)["\'][^>]*(?:sizes=["\'](\d+)x\d+["\'])?',
            html,
            re.IGNORECASE,
        )

        # Parse and sort by size (largest first)
        sized_icons = []
        for match in icon_with_sizes:
            if isinstance(match, tuple) and len(match) == 2:
                size_str, href = match
                if href and not size_str:
                    # Reversed order match
                    href, size_str = match
                size = int(size_str) if size_str and size_str.isdigit() else 0
                if href:
                    sized_icons.append((size, href))

        # Sort by size descending, filter for reasonable sizes
        sized_icons.sort(key=lambda x: x[0], reverse=True)
        for size, href in sized_icons:
            if size >= 32:  # Prefer icons 32px or larger
                logo = resolve_url(href)
                logger.info(
                    f"[ONBOARDING] Found icon with size {size}x{size}: {logo}"
                )
                return logo

        return None

    def _find_apple_touch_icon(
        self, html: str, resolve_url: callable
    ) -> str | None:
        """Find apple-touch-icon (usually 180x180 or larger)."""
        apple_patterns = [
            r'<link[^>]*rel=["\']apple-touch-icon(?:-precomposed)?["\'][^>]*href=["\']([^"\']+)["\']',
            r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']apple-touch-icon(?:-precomposed)?["\']',
        ]
        for pattern in apple_patterns:
            apple_match = re.search(pattern, html, re.IGNORECASE)
            if apple_match:
                logo = resolve_url(apple_match.group(1))
                logger.info(f"[ONBOARDING] Found apple-touch-icon: {logo}")
                return logo

        return None

    def _find_favicon_link(
        self, html: str, resolve_url: callable
    ) -> str | None:
        """Find any favicon link."""
        favicon_patterns = [
            r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\']',
            r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:shortcut )?icon["\']',
        ]
        for pattern in favicon_patterns:
            favicon_match = re.search(pattern, html, re.IGNORECASE)
            if favicon_match:
                logo = resolve_url(favicon_match.group(1))
                logger.info(f"[ONBOARDING] Found favicon link: {logo}")
                return logo

        return None

    def _check_common_favicon_paths(
        self, client: httpx.Client, base_url: str
    ) -> str | None:
        """Check common favicon paths."""
        common_paths = [
            "/favicon.ico",
            "/favicon.png",
            "/favicon-32x32.png",
            "/favicon-16x16.png",
            "/apple-touch-icon.png",
        ]
        for path in common_paths:
            favicon_url = f"{base_url}{path}"
            try:
                favicon_response = client.head(favicon_url)
                if favicon_response.status_code == 200:
                    content_type = favicon_response.headers.get("content-type", "")
                    if "image" in content_type or path.endswith(
                        (".ico", ".png", ".svg")
                    ):
                        logger.info(
                            f"[ONBOARDING] Found favicon at common path: {favicon_url}"
                        )
                        return favicon_url
            except Exception:
                pass

        return None

    def _find_og_image(self, html: str, resolve_url: callable) -> str | None:
        """Find og:image as last resort."""
        og_patterns = [
            r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
        ]
        for pattern in og_patterns:
            og_match = re.search(pattern, html, re.IGNORECASE)
            if og_match:
                logo = resolve_url(og_match.group(1))
                logger.info(f"[ONBOARDING] Found og:image (fallback): {logo}")
                return logo

        return None

    def _fetch_logo_from_linkedin(self, linkedin_url: str) -> str | None:
        """
        Fetch logo from LinkedIn company page.

        LinkedIn requires authentication for scraping, so this is limited.
        In production, use LinkedIn API for reliable access.
        """
        logger.info(
            f"[ONBOARDING] LinkedIn logo fetching not implemented: {linkedin_url}"
        )
        return None

    def _fetch_picture_from_linkedin(self, linkedin_url: str) -> str | None:
        """
        Fetch profile picture from LinkedIn profile page.

        LinkedIn blocks most scraping, but we can try to get the og:image
        which sometimes contains the profile picture.
        """
        try:
            # Ensure URL has scheme
            if not linkedin_url.startswith(("http://", "https://")):
                linkedin_url = f"https://{linkedin_url}"

            # Normalize LinkedIn URL
            if "linkedin.com/in/" not in linkedin_url.lower():
                logger.warning(
                    f"[ONBOARDING] Invalid LinkedIn profile URL: {linkedin_url}"
                )
                return None

            with httpx.Client(
                timeout=HTTP_TIMEOUT,
                follow_redirects=True,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                },
            ) as client:
                response = client.get(linkedin_url)
                response.raise_for_status()
                html = response.text

                # Look for og:image which often contains profile picture
                og_patterns = [
                    r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
                    r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
                ]

                for pattern in og_patterns:
                    og_match = re.search(pattern, html, re.IGNORECASE)
                    if og_match:
                        image_url = og_match.group(1)
                        # LinkedIn profile pictures usually contain "profile-displayphoto"
                        # Filter out generic LinkedIn images
                        if (
                            "profile" in image_url.lower()
                            or "media" in image_url.lower()
                        ):
                            logger.info(
                                f"[ONBOARDING] Found LinkedIn profile picture: {image_url[:100]}..."
                            )
                            return image_url

                # Try to find profile image in the HTML directly
                img_patterns = [
                    r'<img[^>]*class=["\'][^"\']*profile-photo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']',
                    r'<img[^>]*src=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*profile-photo[^"\']*["\']',
                    r'<img[^>]*class=["\'][^"\']*pv-top-card[^"\']*["\'][^>]*src=["\']([^"\']+)["\']',
                ]

                for pattern in img_patterns:
                    img_match = re.search(pattern, html, re.IGNORECASE)
                    if img_match:
                        image_url = img_match.group(1)
                        logger.info(
                            f"[ONBOARDING] Found LinkedIn profile image: {image_url[:100]}..."
                        )
                        return image_url

        except httpx.HTTPStatusError as e:
            logger.warning(
                f"[ONBOARDING] LinkedIn returned {e.response.status_code} for {linkedin_url}"
            )
        except Exception as e:
            logger.warning(
                f"[ONBOARDING] Error fetching profile picture from LinkedIn: {e}"
            )

        return None


# Singleton instance
asset_fetcher_service = AssetFetcherService()
