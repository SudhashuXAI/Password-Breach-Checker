from project import sha 
from project import sha_split 
from project import find_suffix


def test_sha():
    assert sha("hello")=="AAF4C61DDCC5E8A2DABEDE0F3B482CD9AEA9434D"

def test_sha_split():
    assert sha_split("AAF4C61DDCC5E8A2DABEDE0F3B482CD9AEA9434D") == ("AAF4C","61DDCC5E8A2DABEDE0F3B482CD9AEA9434D")

def test_find_suffix():
    fake_data = "ABCDE:10\nFGHIJ:5\nKLMNO:2"
    assert find_suffix(fake_data,"FGHIJ") == "5"      