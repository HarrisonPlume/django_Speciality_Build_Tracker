from django.dispatch import receiver
from .signals import Part_Saved
from .models import Part

@receiver(Part_Saved)
def CreateParts(sender, **kwargs):
    """
    Function takes the input setials and creates multiple parts 
    """
    obj = Part.objects.latest("pub_date")
    serials = obj.serial
    serials = serials.split("-")
    Component_Prep_tasks = obj.Component_Prep_tasks.all()
    Stacking_tasks = obj.Stacking_tasks.all()
    Forming_tasks = obj.Forming_tasks.all()
    Wire_Cut_tasks = obj.Wire_Cut_tasks.all()
    Pitching_tasks = obj.Pitching_tasks.all()
    Header_Plate_tasks = obj.Header_Plate_tasks.all()
    Deburr_tasks = obj.Deburr_tasks.all()
    Plating_tasks = obj.Plating_tasks.all()
    PartTitle = obj.title
    if len(serials) > 1:
        firstserial = int(serials[0])
        lastserial = int(serials[1])
        for serial in range(firstserial, lastserial+1):
            Part.objects.create(title = obj.title, serial = serial,team = obj.team)
            newpart = Part.objects.get(title = PartTitle, serial =serial)
            newpart.Component_Prep_tasks.set(Component_Prep_tasks)
            newpart.Stacking_tasks.set(Stacking_tasks)
            newpart.Forming_tasks.set(Forming_tasks)
            newpart.Wire_Cut_tasks.set(Wire_Cut_tasks)
            newpart.Pitching_tasks.set(Pitching_tasks)
            newpart.Header_Plate_tasks.set(Header_Plate_tasks)
            newpart.Deburr_tasks.set(Deburr_tasks)
            newpart.Plating_tasks.set(Plating_tasks)
            newpart.save()
        obj.delete()
    else:
        return
    
