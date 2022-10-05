from datefinder import find_dates
from datetime import datetime,timedelta

class ParseTimeTable():
    '''
    Parses the time-table provided in V-TOP and \n
    returns list of lectures with list of details of respective lecture.\n
    Details include:\n
    course,faculty,slot,course_type,category,class_number,LTPJC\n
    All of this will be parsed from raw text copied from the Time-Table page on V-TOP
    '''
    def __init__(self):
        '''
        Constructor for ParseTimeTable\n
        Initializes:
            number_of_cols=14
            "start_times" for each lecture
            "slot_details" as the day and timing they belong to
            "days" from Monday to Sunday
        '''
        self.number_of_cols = 14
        self.thoery_duration = 50
        self.start_times = (
            # '08:00', '08:55', '09:50', '10:45', '11:40', '12:35', '14:00', '14:55', '15:50', '16:50', '17:40', '18:35',
            '08:30 AM', '10:05 AM', '11:40 AM', '13:15 PM', '14:50 PM', '16:25 PM', '18:00 PM',
        )
        # day_index: 0-6 where 0 => Monday
        # "slot":[[day_index,start_time_index],]
        self.slot_details = {
            # Theory
            "A11":[[0,0]],"A12":[[2,0]],"A13":[[4,0]],"A14":[[5,0]],"A21":[[0,3]],"A22":[[2,3]],"A23":[[4,3]]
            "B11":[[0,1]],"B12":[[2,1]],"B13":[[4,1]],"B14":[[5,1]],"B21":[[0,5]],"B22":[[2,5]],"B23":[[3,4]],
            "C11":[[0,2]],"C12":[[2,2]],"C13":[[4,2]],"C14":[[5,2]],"C21":[[0,6]],"C22":[[2,6]],"C23":[[1,4]],
            "D21":[[1,3]],"D22":[[3,3]],"D23":[[4,6]],
            "E11":[[1,1]],"E12":[[3,1]],"E13":[[0,4]],
            "F11":[[1,2]],"F12":[[3,2]],"F13":[[2,4]],
        }
        self.days = ['']*7       
    
    
    def addDatesToDaysList(self, date):
        '''
        Replaces the dates that belongs to their respective days\n
        with the items in the list "days"\n
        Parameters:
            date: str
        Returns:
            -1 if Error, otherwise 0
        '''
        try:
            dt = list(find_dates(date))
        except Exception as e:
            print(str(e))
            return -1
        if(len(dt)==0):
            print("Error in ParseTimeTable.py addDatesToDaysList() function:\nlength of possible dates list = 0")
            return -1
        dt = dt[0]
        self.days = ['']*7
        for i in range(7):
            self.days[dt.weekday()] = dt.strftime("%d %B %Y")
            dt += timedelta(days=1)
        return 0


    def parseTT(self, data):
        '''
        Converts Raw data provided as text to a list of lectures\n
        with details like slot,title,location,description,duration,popup\n
        Parameters:
            data: str
        Returns:
            list(list)
        '''
        data = list(filter(lambda a: a != '',[x.rstrip() for x in data.split('\n')]))
        """
        data -> '1', 'General (Semester)', 'STS2102 - Enhancing Problem Solving Skills - Soft Skill', '0 0 0 0 1', 'University Core', 'Regular', 'CH2019205000291', 'F1+TF1', 'AB1-408', 'SMART (APT) - ACAD', '01-Nov-2019 14:06', '02-Nov-2019', '- Manual', 'Registered and Approved', '2', ...
        """
        parsedTimeTable = list()
        for i in range(len(data)//self.number_of_cols):
            course_code, course, course_type = data[2].split(" - ")
            LTPJC = data[3]
            category = data[4]
            class_number = data[5]
            slots = [data[6]]
            slots = data[6].split('+')
            venue = data[7]
            faculty = data[8]
            data = data[self.number_of_cols:]
            # Avoid Projects as they have the same slot as Theory and causes problem later
            # LazyProgrammer :P
            for slot in slots:
                title = course_code
                location = venue
                description = "\n".join([course,faculty,"Slot: "+slot,course_type,category,"Class Number: "+class_number,"L T P J C",LTPJC,])
                duration = self.thoery_duration
                popup = duration//10
                parsedTimeTable.append([slot,title,location,description,duration,popup])
        return parsedTimeTable
    

    def convertTTtoEvents(self,data,date):
        '''
        Converts the Time-Table provided in Raw Text to \n
        list of Events, ready to be added as Events using Calendar API\n
        Format of events:
            datetime, title, location, description, duration, popup
        Parameters:
            data: str :- Raw Text Time-Table
            date: str :- Start Date for the Events to be added
        Returns:
            list(list)
        '''
        try:
            if(self.addDatesToDaysList(date)==-1):
                raise(Exception("Error in addDatesToDaysList() function"))
            parsed_data = list()
            parsedTimeTable = self.parseTT(data)
            for lecture in parsedTimeTable:
                for indices in self.slot_details[lecture[0]]:
                    start_time = list(find_dates(self.days[indices[0]]+' '+self.start_times[indices[1]]))
                    if(len(start_time)>0):
                        start_time = start_time[0]
                    else:
                        raise(Exception("Couldn't find match for start_time"))
                    parsed_data.append([start_time]+lecture[1:])
            return parsed_data
        except Exception as e:
            raise(Exception("Error in ParseTimeTable.py convertTTtoEvents():"+str(e)))
