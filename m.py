# ================= PAGES =================
    async def pages(self, chapter_id: str):
        url = f"{self.api_url}/chapters/{chapter_id}"

        params = {
            "selected_language": "pt-br"
        }

        async with httpx.AsyncClient(
            headers=self.headers,
            timeout=self.timeout,
            http2=False
        ) as client:

            r = await client.get(url, params=params)

            if r.status_code != 200:
                print("Pages error:", r.status_code, r.text)
                return []

            data = r.json()

        chapter_data = data.get("data", {})

        cdn = chapter_data.get("cdn")
        images = chapter_data.get("images", [])

        if not cdn or not images:
            return []

        pages = []

        for img in images:
            path = img.get("path") or img.get("url") or img.get("image")
            if not path:
                continue

            if path.startswith("http"):
                pages.append(path)
            else:
                pages.append(f"{cdn}/{path}")

        return pages
