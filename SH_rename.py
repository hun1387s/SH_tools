import maya.cmds as cmds
import pymel.core as pm
import string


class UndoContext(object):
    def __enter__(self):
        cmds.undoInfo(openChunk=True)
    def __exit__(self, *exc_info):
        cmds.undoInfo(closeChunk=True)


def rename_script(frontText, frontText_1, ComboBox, backText):
    with UndoContext():
        selobj = pm.ls(sl=1)
        var_lower_alpha = list(string.ascii_lowercase)
        var_upper_alpha = list(string.ascii_uppercase)
        one_Var = list(range(10))
        ten_Var = list(range(10))
        han_Var = list(range(10))
        var_number = []
        for _100num in han_Var:
            if len(selobj) < 100:
                for _10num in ten_Var:
                    for _1num in one_Var:
                        num = str(_10num) + str(_1num)
                        var_number.append(num)
            else:
                for _10num in ten_Var:
                    for _1num in one_Var:
                        num = str(_100num) + str(_10num) + str(_1num)
                        var_number.append(num)

        if ComboBox in "[00-99]":
            _combo = var_number
        elif ComboBox in "[a-z]":
            _combo = var_lower_alpha
        elif ComboBox in "[A-Z]":
            _combo = var_upper_alpha

        if ComboBox in "None":
            for _num in range(len(selobj)):
                beforName = selobj[_num].shortName()
                selobj[_num].rename("%s%s%s" % (frontText, frontText_1, backText))
                print("Rename : [%s] => [%s%s]" % (beforName, frontText, backText))
        else:
            for _num in range(len(selobj)):
                beforName = selobj[_num].shortName()
                selobj[_num].rename("%s%s%s%s" % (frontText, frontText_1, _combo[_num], backText))
                print("Rename : [%s] => [%s%s%s]" % (beforName, frontText, _combo[_num], backText))


def replace_script(beforeText, afterText):
    with UndoContext():
        selobj = pm.ls(sl=1)

        indexVar = []
        beforeVar = []
        for i, _obj in enumerate(selobj):
            if beforeText in _obj.shortName():
                indexVar.append(i)
                if "|" in _obj.shortName():
                    _divide = _obj.shortName().split("|")
                    print(_divide)
                    beforeVar.append(_divide[-1])
                else:
                    beforeVar.append(_obj)

        afterVar = []
        for _obj in beforeVar:
            _var = _obj.replace(beforeText, afterText)
            afterVar.append(_var)

        for i, _af in zip(indexVar, afterVar):
            beforeName = selobj[i].shortName()
            selobj[i].rename(_af)
            print("Replace : [%s] => [%s]" % (beforeName, _af))


def prefix_script(prefix):
    with UndoContext():
        selobj = pm.ls(sl=1)
        beforeVar = []
        for _obj in selobj:
            if "|" in str(_obj):
                _divide = _obj.shortName().split("|")
                print(_divide)
                beforeVar.append(_divide[-1])
            else:
                beforeVar.append(_obj.shortName())

        for _obj, _name in zip(selobj, beforeVar):
            beforeName = _obj.shortName()
            _obj.rename(prefix + _name)
            print("Prefix : [%s] => [%s]" % (beforeName, _name))


def suffix_script(suffix):
    with UndoContext():
        selobj = pm.ls(sl=1)
        beforeVar = []
        for _obj in selobj:
            if "|" in str(_obj):
                _divide = _obj.shortName().split("|")
                print(_divide)
                beforeVar.append(_divide[-1])
            else:
                beforeVar.append(_obj.shortName())

        for _obj, _name in zip(selobj, beforeVar):
            beforeName = _obj.shortName()
            _obj.rename(_name + suffix)
            print("Suffix : [%s] => [%s]" % (beforeName, _name))

