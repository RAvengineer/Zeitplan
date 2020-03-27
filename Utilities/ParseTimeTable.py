class ParseTimeTable():
    def __init__(self):
        self.tt = dict()
        self.number_of_cols = 14
    
    def readTT(self, data):
        data = list(filter(lambda a: a != '',[x.rstrip() for x in data.split('\n')]))
        """
        data -> '1', 'General (Semester)', 'STS2102 - Enhancing Problem Solving Skills - Soft Skill', '0 0 0 0 1', 'University Core', 'Regular', 'CH2019205000291', 'F1+TF1', 'AB1-408', 'SMART (APT) - ACAD', '01-Nov-2019 14:06', '02-Nov-2019', '- Manual', 'Registered and Approved', '2', ...
        """
        parsedTimeTable = list()
        for i in range(len(data)//self.number_of_cols):
            course_code, course, course_type = data[2].split(" - ")
            LTPJC = data[3]
            category = data[4]
            class_number = data[6]
            slots = [data[7]]
            if(course_type!="Embedded Lab"):
                slots = data[7].split('+')
            venue = data[8]
            faculty = data[9]
            data = data[self.number_of_cols:]
            # Avoid Projects as they have the same slot as Theory and causes problem later
            # LazyProgrammer :P
            if(course_type=="Embedded Project"):
                continue
            for slot in slots:
                title = course_code
                location = venue
                description = "\n".join([course,faculty,"Slot: "+slot,course_type,category,"Class Number: "+class_number,"L T P J C",LTPJC,])
                duration = 50
                if(slot[0]=='L'):
                    duration = 100
                popup = duration//10
                parsedTimeTable.append([slot,title,location,description,duration,popup])
        return parsedTimeTable
