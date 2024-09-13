def multi_page_option_selection_menu(selection_name: str, options: list, page_number: int = 0):
    """
    Display a menu for selecting an option from a list that may span multiple pages.
    Args:
        selection_name: The name of the selection.
        options: The list of options to select from.
        page_number: The current page number.

    Returns:
        The selected option or None if the user chooses to return to the previous menu.
    """
    options_on_page = options[page_number * 9:page_number * 9 + 9]
    total_pages = len(options) // 9 + 1
    print(f"--- Please select a {selection_name} ---")
    for i, option in enumerate(options_on_page):
        print(f"{i + 1}: {option}")
    if total_pages > 1:
        print("n: Next page")
        print("p: Previous page")
    print("q: Return to previous menu")
    print(f"Page {page_number + 1} / {total_pages}")
    user_selection = input()
    match user_selection:
        case "n" if len(options) > (page_number + 1) * 9:
            return multi_page_option_selection_menu(selection_name, options, page_number + 1)
        case "n":
            print("No more pages. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)
        case "p" if page_number > 0:
            return multi_page_option_selection_menu(selection_name, options, page_number - 1)
        case "p":
            print("No previous pages. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)
        case "q":
            return None
        case _ if user_selection.isdigit():
            selection_index = int(user_selection) - 1
            if selection_index < len(options_on_page):
                return options_on_page[selection_index]
            else:
                print("Invalid selection. Please try again.")
                return multi_page_option_selection_menu(selection_name, options, page_number)
        case _:
            print("Invalid selection. Please try again.")
            return multi_page_option_selection_menu(selection_name, options, page_number)