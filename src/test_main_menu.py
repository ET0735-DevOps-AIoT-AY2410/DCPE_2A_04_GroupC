def test_main_menu_option1():
    import main_menu
    option = 1
    main_menu.handle_user_selection(option)

    assert main_menu.testValue == 3