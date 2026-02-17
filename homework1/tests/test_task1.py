import task1

def test_task1(capsys):
    task1.main()
    std = capsys.readouterr()
    assert std.out == "Hello, World!\n"
