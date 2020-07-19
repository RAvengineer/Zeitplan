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
        self.lab_duration = 100
        self.start_times = (
            # '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00',
            '08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM',
        )
        # day_index: 0-6 where 0 => Monday
        # "slot":[[day_index,start_time_index],]
        self.slot_details = {
            # Theory
            'A1': [[0, 0], [1, 1], [2, 2]], 'A2': [[0, 6], [1, 7], [2, 8]], 
            'B1': [[1, 0], [2, 1], [3, 2]], 'B2': [[1, 6], [2, 7], [3, 8]], 
            'C1': [[2, 0], [3, 1], [4, 2]], 'C2': [[2, 6], [3, 7], [4, 8]], 
            'D1': [[3, 0], [4, 1], [5, 2]], 'D2': [[3, 6], [4, 7], [5, 8]], 
            'E1': [[0, 3], [4, 0], [5, 1]], 'E2': [[0, 9], [4, 6], [5, 7]], 
            'F1': [[0, 2], [1, 3], [5, 0]], 'F2': [[0, 8], [1, 9], [5, 6]], 
            'G1': [[0, 1], [1, 2], [2, 3]], 'G2': [[0, 7], [1, 8], [2, 9]], 
            'TA1': [[3, 3]], 'TA2': [[3, 9]], 
            'TB1': [[4, 3]], 'TB2': [[4, 9]], 
            'TC1': [[5, 3]], 'TC2': [[5, 9]],  
            'TD1': [[0, 4]], 'TD2': [[0, 10]], 
            'TE1': [[1, 4]], 'TE2': [[1, 10]], 
            'TF1': [[2, 4]], 'TF2': [[2, 10]], 
            'TAA1': [[4, 4]], 'TAA2': [[4, 10]], 
            'TBB1': [[5, 4]], 'TBB2': [[5, 10]], 
            'TCC1': [[0, 5]], 'TCC2': [[0, 11]],
            'TDD1': [[1, 5]], 'TDD2': [[1, 11]], 
            'TEE1': [[2, 5]], 'TEE2': [[2, 11]], 
            'TFF1': [[3, 5]], 'TFF2': [[3, 11]], 
            'S1': [[3, 4]], 'S2': [[4, 5]], 
            'S3': [[5, 5]], 'S4': [[3, 10]], 
            'S5': [[4, 11]], 'S6': [[5, 11]],
            # Lab
            'L1+L2+L3': [[0, 0]], 'L4+L5+L6': [[0, 3]], 'L37+L38+L39': [[0, 6]], 'L40+L41+L42': [[0, 9]], 
            'L7+L8+L9': [[1, 0]], 'L10+L11+L12': [[1, 3]], 'L43+L44+L45': [[1, 6]], 'L46+L47+L48': [[1, 9]], 
            'L13+L14+L15': [[2, 0]], 'L16+L17+L18': [[2, 3]], 'L49+L50+L51': [[2, 6]], 'L52+L53+L54': [[2, 9]], 
            'L19+L20+L21': [[3, 0]], 'L22+L23+L24': [[3, 3]], 'L55+L56+L57': [[3, 6]], 'L58+L59+L60': [[3, 9]], 
            'L25+L26+L27': [[4, 0]], 'L28+L29+L30': [[4, 3]], 'L61+L62+L63': [[4, 6]], 'L64+L65+L66': [[4, 9]], 
            'L31+L32+L33': [[5, 0]], 'L34+L35+L36': [[5, 3]], 'L67+L68+L69': [[5, 6]], 'L70+L71+L72': [[5, 9]],           
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
                duration = self.thoery_duration
                if(slot[0]=='L'):
                    duration = self.lab_duration
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
