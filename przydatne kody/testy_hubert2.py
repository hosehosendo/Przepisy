def add_buttons_tab1():

    button_frame_tab1 = LabelFrame(tab2, text="Commands")
    button_frame_tab1.pack(fill="x", expand="yes", padx=20)

    update_button = Button(button_frame_tab1, text="Update Record", command=update_record)
    update_button.grid(row=0, column=0, padx=10, pady=10)

    add_button = Button(button_frame_tab1, text="Add Record", command=add_record)
    add_button.grid(row=0, column=1, padx=10, pady=10)

    remove_one_button = Button(button_frame_tab1, text="Remove One Selected", command=remove_one)
    remove_one_button.grid(row=0, column=3, padx=10, pady=10)

    # Bind the treeview
    my_tree.bind("<ButtonRelease-1>", select_record)