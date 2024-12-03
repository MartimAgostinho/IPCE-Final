#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
------------------------------------------------------
max width = 100 columns
tab = 4 spaces
01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
------------------------------------------------------

------------------------------------------------------
Introdução à Programação para a Ciência e Engenharia - Projeto de 2024/2025

*** Datas & Cronologias ***

Calendário gregoriano proléptico

 AUTHORS IDENTIFICATION
	Estudante 1: 70392, Martim Agostinho
	Estudante 2: 70404, Nuno dos Reis

Comments:
......................................
......................................
...................................
......................................

Place here the numbers and names of the authors, plus possibly some comments.
Do not deliver an anonymous file with unknown authors.
------------------------------------------------------

======================================================
CHANGELOG:
20/nov - Foi alterada a ordem dos nomes em VARIABLE_HOLIDAYS_NAMES
18/nov - Adicionado "@staticmethod" na função Util.error.
18/nov - Adicionados comentários em alguns métodos que não tinham comentário.
18/nov - Removida a função Date.move_year, que ficou esquecida duma experiência que foi feita. Mas se alguém descobrir alguma utilidade para essa função, pode deixar ficar, claro.
======================================================

"""
from __future__ import annotations

class Util:
    @staticmethod
    def file_exists(file_name: str) -> bool:
        """ Check if a file can be opened in read mode. """
        try:
           f = open(file_name, 'r')
           f.close()
           return True
        except FileNotFoundError:
           return False
    
    @staticmethod
    def error(mesg: str):
        """ Issue an error message. """
        print("ERRO:", mesg)


class DateFormats:
    WEEK_NAMES = [
            "Domingo", "Segunda-feira", "Terça-feira",
            "Quarta-feira", "Quinta-feira",
            "Sexta-feira", "Sábado"]

    VARIABLE_HOLIDAYS_NAMES = [
        "Carnaval", "Sexta-feira Santa", "Páscoa", "Corpo de Cristo"]

    @staticmethod
    def from_str(s: str) -> Date:
        """ Build a date from a string.
            If the format is invalid or the date is invalid then return None.
        """
        l = s.split("/")
        valid_format = (
                len(l) == 3
            and l[0].isdigit()
            and l[1].isdigit()
            and len(l[2]) > 0
            and (l[2][1:].isdigit() if l[2][0] == '-' else l[2].isdigit())
         )
        if not valid_format:
            return None
        day, month, year = [int(x) for x in l]
        d = Date(day, month, year)
        if not d.is_valid():
            return None
        return d

    @staticmethod
    def to_str(d: Date) -> str:
        """ Convert a date to a formated string. """
        return f"{d.day}/{d.month}/{d.year}"
        
    @staticmethod
    def cal_month(month, year) -> str:
        """ Generate the calendar for a given month and year. """
        return ""
        
    @staticmethod
    def cal_year(year: int) -> str:
        """ Generate the full calendar for a given year. """
        return ""


class Date:
    # Constants shared by all the methods
    PERIOD_YEARS = 400
    PERIOD_DAYS = PERIOD_YEARS * 365 + 97
    SUN, MON, TUE, WED, THU, FRI, SAT = range(7)

    # Variables shared by all the methods
    fixed_holidays = None
    chrons         = None
    # Static methods - functions without "self"

    @staticmethod
    def set_fixed_holidays(h: Chronology):
        """ Setup the variable 'fixed_holidays'.
            Must call this function before start using any
            methods related to holidays. """
        Date.fixed_holidays = h

    @staticmethod
    def is_zero(year: int) -> bool:  # PRIVATE
        """ Check for the invalid year zero? """
        return year == 0;
    
    @staticmethod
    def is_bc(year: int) -> bool:  # PRIVATE
        """ Check for a negative date - before Christ? """
        return year < 0;
    
    @staticmethod
    def is_leap(year: int) -> bool:
        """ Check if the year is a leap year.
            Precondition: not is_zero(year)
        """
        if Date.is_zero(year):
            return False
   
        return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))
    
    @staticmethod
    def month_length(month: int, year: int) -> int:
        """ Number of days of a given month (in a given year).
            Precondition: 1 <= month <= 12 and not is_zero(year)
        """
        if month < 1 or month > 12 or Date.is_zero(year):
            return 0
        
        if month == 2:
            if Date.is_leap(year):
                return 29
            else: return 28
       
        if month in [4, 6, 9, 11]: 
            return 30

        return 31      

    @staticmethod
    def from_str(s: str) -> Date:
        """ Build a date from a string.
            If the date is invalid then return None.
        """
        laux = s.split('/')
        if len(laux) != 3:
            return None
        
        #day, month, year = map(int, laux)
        
        try :
            day, month, year = map(int, laux)
        except:
            return None
        
        new_date = Date(day, month, year)

        if not Date.is_valid(new_date):
            return None

        return new_date
    
    @staticmethod
    def today() -> Date:
        """ Today's date. """
        from time import strftime
        return DateFormats.from_str(strftime("%d/%m/%Y"))
 
    @staticmethod
    def easter(year: int) -> Date:
        """ Date of easter for a given year.
            Precondition: year > 0
            Sources:
                https://aa.usno.navy.mil/faq/easter
                https://adsabs.harvard.edu/full/1940BuAst..12..391O
        """
        y = year
        c = y // 100
        n = y - 19 * (y // 19)
        k = (c - 17) // 25
        i = c - c // 4 - (c - k) // 3 + 19 * n + 15
        i = i - 30 * (i // 30)
        i = i - (i // 28) * (1 - (i // 28)
                             * (29 // (i + 1)) * ((21 - n) // 11))
        j = y + y // 4 + i + 2 - c + c // 4
        j = j - 7 * (j // 7)
        l = i - j
        m = 3 + (l + 40) // 44
        d = l + 28 - 31 * (m // 4)
        return Date(d, m, y)

    @staticmethod
    def variable_holidays(year: int) -> Chronology:  # PRIVATE
        """ Build the Chronology of the variable holidays for a given year.
            Precondition: year > 0
        """
        if year <= 0:
            return None
        
        easter = Date.easter(year)
        
        d = dict()
        d["Páscoa"] = easter

        aux = easter
        for n in range(47):
            aux = Date.prev(aux)

        d["Carnaval"] = aux

        aux = easter
        for n in range(2):
            aux = Date.prev(aux)

        d["Sexta-feira Santa"] = aux
        
        aux = easter
        for n in range(60):
            aux = Date.next(aux)

        d["Corpo de Deus"] = aux

        return Chronology(d)
 
    @staticmethod
    def fridays13(year: int) -> list[Date]:
        """ The list of all the fridays 13 dates for a given year.
            Precondition: 0 < year
        """
        if Date.is_zero(year):
            return None

        fridays_vec = []

        for  month in range(1,13):
            date = Date(13,month,year)
            if Date.day_of_the_week(date) == 5:
                fridays_vec.append(date)
        return fridays_vec

    @staticmethod
    def monthNum2Str( month: int ):
        if month < 1 or month > 12:
            return None
        m = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]    
        return m[month - 1]

    #FIXME Debug 
    def print(self :Date):
        print( f"Dia: {self.day}, Month: { self.month }, Ano: {self.year}" )

    def bc_Gregorian(year: int) -> bool:
        """ checks if the Date ir before   """

    def next_week_day(week_day: int) -> int:
        """ Returns the next week day.
            Precondition: 0 <= week day <= 6
        """
        if week_day < 0 or week_day > 6:
            return None
        
        if week_day == 6:
            week_day = 0
        else: week_day += 1

        return week_day
    
    def prev_week_day(week_day: int) -> int:
        """ Returns the prev week day.
            Precondition: 0 <= week day <= 6
        """
        if week_day < 0 or week_day > 6:
            return None
        
        if week_day == 0:
            week_day = 6
        else: week_day -= 1

        return week_day

    def todays_date()->Date:
        """ Shows todays date.
            Precondition: none
        """     
        return Date.today()  

    def count_days(month: int, year: int)->int:
        """ Returns the number of days of a specific
            month from a specific year (n = 0 -> all year).
            Precondition: 1 <= month <= 12 {\0} and year > 0
        """

        if year <= 0:
            return None
        
        if month == 0:
            if Date.is_leap(year): return 366
            else: return 365
        else:
            if 1 <= month <= 12: return Date.month_length(month, year)
            else: return None

    def show_commands():
       #Returns a list of available commands with their inputs.

        commands = [
        {"name": "Mais", "input": "d, n"},
        {"name": "Menos", "input": "d1, d2"},
        {"name": "Autores", "input": "-"},
        {"name": "Ajuda", "input": "-"},
        {"name": "Calendário", "input": "m, a"},
        {"name": "Dias", "input": "m, a"},
        {"name": "Feriados", "input": "m, a"},
        {"name": "Hoje", "input": "-"},
        {"name": "Idade", "input": "d"},
        {"name": "Férias máximas", "input": "-"},
        {"name": "Dia de semana", "input": "d"},
        {"name": "Sextas-feiras 13", "input": "a"},
        {"name": "Carrega", "input": "f, s"},
        {"name": "Mostra", "input": "s"},
        {"name": "Repetidas", "input": "s1, s2"},
        {"name": "Feriados 2", "input": "s1, s2"},
        {"name": "União", "input": "s1, s2, s3"},
        {"name": "Interseção por data", "input": "s1, s2, s3"},
        {"name": "Quit", "input": "-"}
        ]
        return commands
 
    def show_month(year: int, month: int):
        """ Returns the calender of a specific
            month .
            Precondition: 1 <= month <= 12 {\0} and year > 0
        """
        M_lines = 8
        M_cols  = 20
        day     = 1

        year_str = str(year)
        month_str = Date.monthNum2Str(month)
        m = [ [ ' ' for _ in range(M_cols) ] for _ in range(M_lines) ]
        if year_str != '':
            month_str += " " + year_str

        for i in range(len(month_str)):
            m[0][i] = month_str[i]
        
        straux = "Do Sg Te Qa Qi Sx Sa"
        for i in range(len(straux)):
            m[1][i] = straux[i]

        FirstWeekDay = Date.day_of_the_week(Date(1, month, year)) + 1
        LastDayMonth = Date.month_length(month, year)

        for i in range(FirstWeekDay ,int(M_cols/3) + 2):
            m[2][i*3 - 2] = str( day )
            day +=1

        for i in range(3,M_lines):
            for j in range(0,7*3,3):
                #m[i][j] = str(day)
                if day >= 10: 
                    straux = str(day)
                    m[i][j] = straux[0]
                    m[i][1 + j] = straux[1]
                else:
                    m[i][j+1] = str(day)
                day += 1
                if day > LastDayMonth:
                    return m

    def show_year(year: int, month :int):
        """ Returns the calender of a specific year .
            Precondition: 1 <= month <= 12 {\0} and year > 0
        """ 
        ColLen      = 66
        LinLen      = 36
        yearmatrix  = [ [ ' ' for _ in range(ColLen) ] for _ in range(LinLen) ]

        yearmatrix[0][0]  = str(year)
        month = 0
        
        for i in range(0,12,3):
            # i month
            # j month col
            mAux = []
            for j in range( 3 ):
                mAux = Date.show_month(year, month + 1)                 
                #l line 
                #c col
                for l in range(8):
                    for c in range(20):
                        yearmatrix[ int(i/3)* 9 + l + 1 ][j*( 22 ) + c] = mAux[l][c] 

                month += 1 

        return yearmatrix
  
    def show_year_month(year: int, month: int):
        """ Returns the calender of a specific year/month .
            Precondition: 1 <= month <= 12 {\0} and year > 0
        """   
        if year <= 0:
            return None
        
        if month == 0:
            return Date.show_year(year, month)
        else:
            if 1 <= month <= 12: return Date.show_month(year, month)
            else: return None

    def print_matrix(month_matrix:list[list[str]]):
        for line in month_matrix:
            for s in line:
                print(s,end='')
            print()
    
    @staticmethod
    def Load_chronology(file_name: str,id: str)-> int: 

        '''Preconditions
            file_name -> File Exists 
        '''
        
        if Date.chrons is None:
            Date.chrons = Chronologies()

        Date.chrons.load( id,file_name )
        return len(Date.chrons.cronos[id].events)
        #print(f"Foram carregados {len(chrons.cronos[id])} elementos.")

    '''
    def read_file():
        f = open('feriados_fixos.txt', 'r', encoding="utf-8")
        Fclean = []
        for line in f:
            StrAux = ''

            for i in range(len(line)):
                if line[i] == '#':
                    StrAux += '\n'
                    break

                StrAux += line[i]

            if StrAux[:-1].strip() != "":
                Fclean.append(StrAux[:-1])

        for line in Fclean:
            
            tokens = line.split(' ')

            if len(tokens) < 2:
                continue

            date = tokens[0]
            
            #If its not a date or doesnt have a name
            if(not Date.is_valid()  ):
                continue
            
            d = Date()
            name = ''.join(tokens[1:])

        f.close()
        Date.fixed_holidays = Fclean
        return None
    '''
    # Instance methods - functions with "self"---------------------------------------------------------------------------
    
    def __init__(self: Date, day: int, month: int, year: int):
        """ Initialize a date. """
        self.day    = day
        self.month  = month
        self.year   = year

    def copy(self: Date) -> Date:
        """ Duplicate a date. """
        return Date(self.day, self.month, self.year)
    
    def is_valid(self: Date) -> bool:  # PRIVATE
        """ Is the date valid? DEVE FALTAR CENAS"""
        
        if Date.is_zero(self.year):
            return False

        if self.month < 0 or self.month > 12:
            return False
        
        if self.day > Date.month_length( self.month,self.year ) or self.day < 0:        
            return False
        
        return True
        
    def __repr__(self: Date) -> str:
        """ Convert date to string. """
        return DateFormats.to_str(self)
           
    def __lt__(self: Date, other: Date) -> bool: #acho que esta torto
        """ Check if self < other.
            Precondition: self.is_valid() and other.is_valid()
        """
        if not Date.is_valid(self) or not Date.is_valid(other):
            return False
        
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day < other.day:
                    return True
            
        return False
    
    def __eq__(self: Date, other: Date) -> bool:
        """ Check if self == other.
            Precondition: self.is_valid() and other.is_valid()
        """
        if not Date.is_valid(self) or not Date.is_valid(other):
            return False
        
        if self.year == other.year and self.month == other.month and self.day == other.day:
            return True
        
        return False
    
    def __le__(self: Date, other: Date) -> bool:
        """ Check if self <= other.
            Precondition: self.is_valid() and other.is_valid()
        """
        if not Date.is_valid(self) or not Date.is_valid(other):
            return False
        
        if self.year < other.year:
            return True
        elif self.year == other.year:
            if self.month < other.month:
                return True
            elif self.month == other.month:
                if self.day <= other.day:
                    return True
        
        return False
    
    def order(self: Date) -> int:
        """ The position of a date within the respective year, starting with 1.
            Precondition: self.is_valid()
        """
        return None
        
    def next(self: Date) -> Date:
        """ Create the date of the next day.
            Precondition: self.is_valid()
        """
        if not Date.is_valid(self):
            return None
        
        day = self.day
        month = self.month
        year = self.year

        if day == Date.month_length(month, year):
            day = 1
            if month == 12:
                month = 1
                year += 1
            else: month += 1
        else: day += 1
        return Date(day, month, year)
    
    def prev(self: Date) -> Date:
        """ Create the date of the previous day.
            Precondition: self.is_valid()
        """
        if not Date.is_valid(self):
            return None
        
        day = self.day
        month = self.month
        year = self.year

        if day == 1:
            if month == 1:
                month = 12
                year -= 1
            else: month -= 1
            day = Date.month_length(month, year)
        else: day -= 1
        return Date(day, month, year)
            
    def move(self: Date, n: int) -> Date:
        """ Create a date shifted n days .
            Precondition: self.is_valid()
        """

        if not self.is_valid():
            return None

        aux_date = Date(self.day, self.month, self.year)

        while n != 0:
            if n < 0:
                aux_date = Date.prev(aux_date)
                n += 1
            else:
                aux_date = Date.next(aux_date)
                n -= 1

        return aux_date

    def distance(self: Date, other: Date) -> int:
        """ Number of days from self to other. Can be negative. .
            Precondition: self.is_valid() and other.is_valid()
        """
        if not self.is_valid() or not other.is_valid():
            return None

        distance = 0

        aux_date = Date(self.day, self.month, self.year)
        if Date.__lt__(self, other):
            while aux_date != other:
                aux_date = Date.next(aux_date)
                distance += 1
        else:   
            while aux_date != other:
                aux_date = Date.prev(aux_date)
                distance -= 1

        return distance

    def age(self: Date) -> int:
        """ The current age in years for somebody that has born in the date self.
            Precondition: self.is_valid() and self <= Date.today()
        """
        if not self.is_valid() or  not Date.__le__(self, Date.today()):
            return None
        
        if self.day == 29 and self.month == 2 and Date.is_leap(self.year):
            aux_date = Date(1, 3, self.year)
        else: aux_date = Date(self.day, self.month, self.year)

        counter = Date.distance(self, Date.today())
        
        age = int(counter / 365.25)
        return age

    def day_of_the_week(self: Date) -> int:
        """ Calculate the day of week of a date.
            Precondition: self.is_valid()
        """
        if not self.is_valid():
            return None
            
        other = Date(1, 1, 2024) #its a monday
        distance = Date.distance(self, other) #esta a dar raia aqui
        week_day = 1

        if distance == 0:
            return week_day
        else:
            for _ in range(abs(distance) % 7):
                if distance > 0:
                    week_day = Date.prev_week_day(week_day)
                else: week_day = Date.next_week_day(week_day)

        return week_day
    
    # Continua - faltam métodos

    
class Chronology:
    def __init__(self: Chronology, events: dict[str, Date]):
        """ Initialize a chronology from a dict. Sort the chronology. """
        self.events = events
        self.sort()      # ensures it is created sorted by key

    @staticmethod
    def from_file(file_name: str) -> Chronology:
         #Util.FileExistsError
        if not Util.file_exists(file_name):
            return None
        
        f = open(file_name, 'r', encoding="utf-8")
        d = dict()

        #Remove all comments, doing it this enable comments at the end of a useful line
        Fclean = []
        for line in f:
            StrAux = ''

            for i in range(len(line)):
                if line[i] == '#':
                    StrAux += '\n'
                    break

                StrAux += line[i]

            if StrAux[:-1].strip() != "":
                Fclean.append(StrAux[:-1])

        for line in Fclean:
            dateStr = ''
            
            for i in range(len(line)):
                
                if line[i] == ' ' or line[i] == '\n':
                    break

                dateStr += line[i]

            name = ''

            #Skip all ' ' before name
            for n in range( i, len(line)):
                if( line[n] != ' ' ):
                    break 

            for j in range( n, len(line)):
                name += line[j]
            if len(name) < 1:
                continue

            date = Date.from_str(dateStr) 
            if date is  None:
                continue

            d[name] = date
            #TODO create cron class 
            #       Add each day
            #       Sort

            #date.print()
            #print(f"Name: {name}")
        
        return Chronology(d)

    def sort(self: Chronology):  # PRIVATE
        """ Sort by key. """

        return None
   
    def __repr__(self: Chronology) -> str:
        """ Convert chronology to string, to display. """
        s = ''
        for e in self.events:
            s += f"\n{e} ---> {self.events[e]}"
        return s[1:]

    def size(self: Chronology):
        """ Size of chronology. """
        return len(self.events)

    def union(self: Chronology, other: Chronology) -> Chronology:
        """ Union of chronologies. """
        return None
    
    # Continua - faltam métodos


class Chronologies:
    def __init__(self: Chronologies):
        """ Initialize a repository of chronologies as empty. """
        self.cronos = dict()
    
    def get(self: Chronologies, id: str) -> Chronology:
        """ Get a named chronology. If it does not exist return None. """
        if id in self.cronos:
            return self.cronos[id]
        else:
            return None
    
    def load(self: Chronologies, id: str, file_name: str):
        """ Load a chronology from file and assign a id to it. """
        self.cronos[id] = Chronology.from_file(file_name)  
    
    def show(self: Chronologies):
        """ Show the contents of the repository, for debuging. """
        for id in self.cronos:
            print(id, "--", self.cronos[id].events)
    
    # Continua - faltam métodos

	
class UI:   # User Interface
    PROG_NAME = "Datas & Cronologias"
    
    def __init__(self: UI):
        """ Initialize a UI with an empty repository of cronologies. """
        self.repository = Chronologies()
    
    def dir(self: UI):
        """ Show the current directory, only for debugging. """
        from os import getcwd
        print(getcwd())
    
    def welcome(self: UI):  # PRIVATE
        """ Print an welcome message. """
        print(UI.PROG_NAME)

    def input_command(self: UI) -> (str, list[str]):  # PRIVATE
        """ Process the command line. """
        command_line = input("> ")
        l = command_line.split()
        if l == []:
            command = ' '
        else:
            command = l[0].upper()
        arguments = l[1:]
        return (command, arguments)
    
    def get_args(self: UI, args: list[str], types: str) -> list[any]:  # PRIVATE
        """ Convert and validate the arguments of any command. """
        error = False
        res = []
        if len(args) != len(types):
            error = True
        else:
            for i in range(len(args)):
                if types[i] == 'd':  # 'd' means Date
                    d = Date.from_str(args[i])
                    if d is None:
                        error = True; break
                    else:
                        res.append(d)
                elif types[i] == 'i':  # 'i' means integer
                    is_int = (args[i][1:].isdigit()
                              if args[i][0] == '-'
                              else args[i].isdigit())
                    if not is_int:
                        error = True; break
                    i = int(args[i])
                    res.append(i)
                elif types[i] == 's':  # 's' means string
                    res.append(args[i])
                else:
                    error = True; break
        if error:
            Util.error("Argumentos inválidos")
            res = ['x']*len(types)     # dummy result with the correct length
        if len(types) == 0:
            return error
        else:
            res.insert(0, error)
            return res
    
    def command_authors(self: UI, args: list[str]):  # PRIVATE
        error = self.get_args(args, "")
        if error: return
        print(UI.PROG_NAME)
        print("Autores: Nuno Reis (70404), Martim Agostinho (70392)")

    def command_plus(self: UI, args: list[str]):  # PRIVATE
        error, d, n = self.get_args(args, "di")
        if error: return
        res = d.move(n)
        print(res)
    
    def command_less(self: UI, args: list[str]):  # PRIVATE
        error, d1, d2 = self.get_args(args, "dd") 
        if error: return
        res = d1.distance(d2)
        print(res)

    def command_help(self: UI, args: list[str]): # PRIVATE
        error = self.get_args(args, "")
        if error: return
        commands = Date.show_commands()
        for res in commands:
            print(f"Comando: {res['name']} | Inputs: {res['input']}")

    def command_days(self: UI, args: list[str]):  # PRIVATE
        error, a, m = self.get_args(args, "ii")
        if error: return
        res = Date.count_days(m, a)
        print(res)

    def command_holidays(self: UI, args: list[str]):
        
        error, a, m = self.get_args(args, "ii")
        if error : return
        if Date.fixed_holidays is None: return
        empty = True
        for k in Date.fixed_holidays.events:
            if m == Date.fixed_holidays.events[k].month:
                print( f"{k} ---> {Date.fixed_holidays.events[k].day}/{m}/{a}" )
                empty = False

        if a > 0:
            VarHol = Date.variable_holidays(a)
            for k in VarHol.events:
                if m == VarHol.events[k].month:
                    print( f"{k} ---> {VarHol.events[k].day}/{m}/{a}" )
                    empty = False
        if empty:
            print("Nada.")
    
    def command_today(self: UI, args: list[str]):  # PRIVATE
        res = Date.todays_date()
        print(res)

    def command_age(self: UI, args:list[str]): #PRIVATE
        error, d = self.get_args(args, "d")
        if error: return
        res = Date.age(d)
        print(res)

    def command_week_day(self: UI, args: list[str]):  # PRIVATE
        error, d = self.get_args(args, "d")
        if error: return
        res = Date.day_of_the_week(d)
        week_days = [
            "Domingo",
            "Segunda-feira",
            "Terça-feira",
            "Quarta-feira",
            "Quinta-feira",
            "Sexta-feira",
            "Sabado"
        ]
        print(week_days[res])

    def command_friday_t(self: UI, args: list[str]):  # PRIVATE
        error, y = self.get_args(args, "i")
        if error: return
        res = Date.fridays13(y)
        for date in res:
            print(date)

    def command_print_calender(self: UI, args: list[str]):
        error, y, m = self.get_args(args, "ii")
        if error: return
        if m < 0 or m > 12:
            return
        matrix = Date.show_year_month(y, m)
        Date.print_matrix(matrix)
        #res = Date.show_months(a, m)
    # Faltam métodos command
    
    def command_upload_chronology(self: UI, args: list[str]):
        
        err,id, file_name = self.get_args( args,"ss" )
        if err: return

        if not Util.file_exists(file_name):
            Util.error(f"Não foi possível abrir o ficheiro \'{file_name}\'")

        n = Date.Load_chronology(file_name,id)

        if n == 0:
            Util.error(f"O ficheiro \'{file_name}\' contém uma cronologia inválida.")
        else:
            print(f"Foram carregados {n} elementos.")

    def command_show_chronology(self: UI,args: list[srt]):
        err,id = self.get_args(args,"s")
        if err:return

        c = Date.chrons.get(id)

        if c is None:
            print("Nada.")
            return
        
        print(repr(c))


    def interpreter(self: UI):
        self.welcome()
        while True:
            command, args = self.input_command()
            if command == '=': self.command_authors(args)
            elif command == '+': self.command_plus(args)
            elif command == '-': self.command_less(args)
            #----------------------------------
            elif command == 'A': self.command_help(args)
            elif command == 'C':self.command_print_calender(args)
            elif command == 'D':self.command_days(args)
            elif command == 'F':self.command_holidays(args)
            #-----------------------
            elif command == 'H': self.command_today(args) 
            elif command == 'I':self.command_age(args) 
            elif command == 'M':self.command_maximum_vacations(args)  #TODO
            elif command == 'S':self.command_week_day(args)  
            elif command == 'T':self.command_friday_t(args) 
            elif command == 'U':self.command_upload_chronology(args)
            elif command == 'V':self.command_show_chronology(args)  
            elif command == 'W':self.command_repeated_chronology(args)  #TODO
            elif command == 'Y':self.command_unity_chronology(args)  #TODO
            elif command == 'Z':self.command_intersection_chronology(args)  #TODO
            # Faltam muitos comandos
            elif command == 'Q': break
            elif command == ' ': pass
            else: Util.error("Comando desconhecido.")
        print("Execução terminada.")
          
    def run(self: UI):
        self.interpreter()

def main():
    ui = UI()
    Date.set_fixed_holidays( Chronology.from_file("feriados_fixos.txt") )
    #Chronology.from_file("Cronologias.txt")
    ui.run()

main()
