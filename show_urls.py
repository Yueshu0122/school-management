from django.urls import get_resolver

def show_urls():
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            for p in pattern.url_patterns:
                print(f"{p.pattern} -> {p.name}")
        else:
            print(f"{pattern.pattern} -> {pattern.name}")

if __name__ == "__main__":
    show_urls() 