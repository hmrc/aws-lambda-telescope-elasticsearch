def get_writable(index: dict) -> bool:
    try:
        try:
            return list(index.get("aliases").values())[0].get("is_write_index")
        except AttributeError:
            return False
    except IndexError:
        return False
