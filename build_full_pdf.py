import base64
import requests
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 805, "TCS-504: System Design — Assignment 1 (Movie Ticket Booking System)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(40, 800, 555, 800)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 25, page_text)
        self.drawString(40, 25, "Confidential — Academic Submission (Semester 5)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 35, 555, 35)
        self.restoreState()

def fetch_mermaid_png(mermaid_code, filename):
    try:
        b64 = base64.b64encode(mermaid_code.encode('utf-8')).decode('ascii')
        url = f"https://mermaid.ink/img/{b64}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Successfully generated diagram: {filename}")
            return filename
    except Exception as e:
        print(f"Failed to fetch mermaid diagram: {e}")
    return None

def build_pdf(output_filename="TCS-504_System_Design_Assignment_1.pdf"):
    # 1. Prepare Mermaid Diagrams
    class_diagram_code = """classDiagram
    direction TB
    class Cinema {
        -name: string
        -screens: vector~Screen~
        +addScreen(screen: Screen): void
        +getScreens(): vector~Screen~
        +getScreen(num: int): Screen*
    }
    class Screen {
        -screenNumber: int
        -screenName: string
        -seats: vector~Seat~
        +addSeat(num: string, type: SeatType): void
        +getSeats(): vector~Seat~
    }
    class Seat {
        -seatNumber: string
        -seatType: SeatType
        +getSeatNumber(): string
        +getSeatType(): SeatType
        +getTypeName(): char*
    }
    class Movie {
        -title: string
        -language: string
        -durationMinutes: int
        +getTitle(): string
        +getLanguage(): string
    }
    class Show {
        -showId: int
        -startTime: string
        -movie: Movie*
        -screen: Screen*
        -showSeats: vector~ShowSeat~
        +findShowSeat(num: string): ShowSeat*
        +bookSeat(num: string): bool
        +releaseSeat(num: string): void
    }
    class ShowSeat {
        -physicalSeat: Seat*
        -seatStatus: SeatStatus
        +isAvailable(): bool
        +bookSeat(): bool
        +releaseSeat(): void
        +getSeatNumber(): string
        +getSeatType(): SeatType
    }
    class Customer {
        -name: string
        -phone: string
        +getName(): string
        +getPhone(): string
    }
    class Booking {
        -bookingId: string
        -customer: Customer*
        -show: Show*
        -bookedSeats: vector~ShowSeat*~
        -totalAmount: double
        -status: BookingStatus
        -nextBookingId: int$
        +markConfirmed(): void
        +markCancelled(): void
        +getBookingId(): string
    }
    class Payment {
        <<abstract>>
        +pay(amount: double)* bool
        +getPaymentMethodName()* char*
    }
    class UpiPayment { +pay(amount: double): bool }
    class CardPayment { +pay(amount: double): bool }
    class CashPayment { +pay(amount: double): bool }
    class PriceCalculator {
        +SILVER_PRICE: double$
        +GOLD_PRICE: double$
        +PLATINUM_PRICE: double$
        +calculateTotal(seats: vector~ShowSeat*~)$ double
    }
    class TicketPrinter {
        +printTicket(b: Booking)$ void
        +printSeatLayout(s: Show)$ void
    }
    class BookingService {
        -bookings: vector~Booking~
        +bookTickets(cust, show, seats, pay): Booking*
        +cancelBooking(id: string): bool
    }
    class SeatCategory {
        <<abstract>>
        +calculateStats(show: Show)* CategoryStats
        +printDetailedStats(show: Show)* void
    }
    class SilverSeatCategory { +printDetailedStats(show: Show): void }
    class GoldSeatCategory { +printDetailedStats(show: Show): void }
    class PlatinumSeatCategory { +printDetailedStats(show: Show): void }

    Cinema "1" *-- "1..*" Screen
    Screen "1" *-- "1..*" Seat
    Show "1" o-- "1" Movie
    Show "1" o-- "1" Screen
    Show "1" *-- "1..*" ShowSeat
    ShowSeat "1" o-- "1" Seat
    Booking "1" o-- "1" Customer
    Booking "1" o-- "1" Show
    Booking "1" o-- "1..*" ShowSeat
    BookingService "1" o-- "*" Booking
    BookingService ..> Payment
    BookingService ..> PriceCalculator
    BookingService ..> TicketPrinter
    Payment <|-- UpiPayment
    Payment <|-- CardPayment
    Payment <|-- CashPayment
    SeatCategory <|-- SilverSeatCategory
    SeatCategory <|-- GoldSeatCategory
    SeatCategory <|-- PlatinumSeatCategory
"""

    sequence_diagram_code = """sequenceDiagram
    autonumber
    actor Customer as customer
    participant UI as cinema_main_menu
    participant BS as bookingService
    participant Show as show
    participant SS as showSeat
    participant PC as priceCalculator
    participant Pay as payment (UPI)
    participant Bk as booking
    participant TP as ticketPrinter

    Customer->>UI: Select Show & Seat ("A1")
    activate UI
    UI->>BS: bookTickets(customer, show, ["A1"], upiPay)
    activate BS
    BS->>Show: findShowSeat("A1")
    activate Show
    Show-->>BS: return showSeat pointer
    deactivate Show
    BS->>SS: isAvailable()
    activate SS
    SS-->>BS: return true (AVAILABLE)
    deactivate SS
    BS->>PC: calculateTotal([showSeat])
    activate PC
    PC-->>BS: return Rs.150
    deactivate PC
    BS->>TP: printSeatPriceBreakdown([showSeat])
    activate TP
    TP-->>BS: breakdown printed
    deactivate TP
    BS->>SS: bookSeat()
    activate SS
    SS-->>BS: return true (BOOKED)
    deactivate SS
    BS->>Pay: pay(150.0)
    activate Pay
    Pay-->>BS: return true (Success)
    deactivate Pay
    BS->>Bk: «create» Booking(cust, show, [showSeat], 150.0)
    activate Bk
    Bk-->>BS: return booking (ID: BK1001)
    deactivate Bk
    BS-->>UI: return booking pointer
    deactivate BS
    UI->>TP: printTicket(booking)
    activate TP
    TP-->>Customer: Display Ticket (BK1001, Rs.150, CONFIRMED)
    deactivate TP
    deactivate UI
"""

    class_img = fetch_mermaid_png(class_diagram_code, "uml_class_diagram.png")
    seq_img = fetch_mermaid_png(sequence_diagram_code, "uml_sequence_diagram.png")

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceAfter=12
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e3a8a")
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1e293b")
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title & Metadata Banner
    banner_data = [
        [
            Paragraph("<b>TCS-504: System Design &mdash; Assignment 1</b>", title_style),
            ""
        ],
        [
            Paragraph("Movie Ticket Booking System (Single Cinema Architecture)", subtitle_style),
            ""
        ],
        [
            Paragraph("<b>Author:</b> Dhruv Bhatt &nbsp;|&nbsp; <b>Branch:</b> B.Tech. CSE (5th Sem)", meta_style),
            Paragraph("<b>Date:</b> 07-Sept-2026 &nbsp;|&nbsp; <b>Code:</b> TCS-504", meta_style)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[330, 185])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (0,1), (1,1)),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 10))

    # Section 1: Scope
    story.append(Paragraph("1. Executive Summary & Problem Scope", h1_style))
    story.append(Paragraph(
        "This project implements a complete Object-Oriented, menu-driven movie ticket booking engine for a single cinema "
        "(e.g., PVR or INOX) in C++14. The system is designed with strict adherence to SOLID design principles, GoF Strategy Pattern, "
        "and Clean Code guidelines under the academic course rule: <i>'One class per file, No header files'</i>.",
        body_style
    ))
    story.append(Paragraph("<b>8 Mandatory Core Features Built (F1 &ndash; F8):</b>", h2_style))
    story.append(Paragraph("&bull; <b>F1:</b> List all movies currently playing with runtime & language.", bullet_style))
    story.append(Paragraph("&bull; <b>F2:</b> For a chosen movie, list its screening shows (auditorium screen + start time).", bullet_style))
    story.append(Paragraph("&bull; <b>F3:</b> For a chosen show, display seat layout with <code>AVAILABLE [ ]</code> / <code>BOOKED [X]</code> status.", bullet_style))
    story.append(Paragraph("&bull; <b>F4:</b> Book one or more seats for a show (atomic validation rejects whole order if any seat is booked).", bullet_style))
    story.append(Paragraph("&bull; <b>F5:</b> Dynamic pricing by tier: <b>SILVER Rs.150</b>, <b>GOLD Rs.250</b>, <b>PLATINUM Rs.400</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>F6:</b> Pay by UPI, Card, or Cash (failed payment aborts booking & triggers atomic seat rollback).", bullet_style))
    story.append(Paragraph("&bull; <b>F7:</b> Print formatted ticket: Booking ID, Movie, Screen, Start Time, Seats, Total Amount, Status.", bullet_style))
    story.append(Paragraph("&bull; <b>F8:</b> Cancel a booking &mdash; all associated seats immediately revert to <code>AVAILABLE</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Bonus (F9):</b> Polymorphic Seat Tier Inspector for real-time tier metrics (Total, Booked, Free).", bullet_style))

    story.append(Spacer(1, 6))

    # Section 2: Step A
    story.append(Paragraph("2. Step A &mdash; Requirement Analysis (FR + NFR)", h1_style))
    story.append(Paragraph("<b>Functional Requirements (FR):</b>", h2_style))
    story.append(Paragraph("&bull; <b>FR1 &mdash; Movie Listing:</b> The system shall list all movies playing with title, language, and duration in minutes.", bullet_style))
    story.append(Paragraph("&bull; <b>FR2 &mdash; Show Scheduling:</b> For any chosen movie, the system shall list scheduled shows with screen name and start time.", bullet_style))
    story.append(Paragraph("&bull; <b>FR3 &mdash; Seat Layout Display:</b> For any chosen show, the system shall display the physical seat layout categorized by tiers (SILVER, GOLD, PLATINUM) with real-time status [ ] (Available) or [X] (Booked).", bullet_style))
    story.append(Paragraph("&bull; <b>FR4 &mdash; Booking (Standard):</b> A customer selects one or more seat numbers for a show. If any selected seat is already BOOKED or invalid, the whole booking is rejected and no seat changes state. Booking is confirmed only after payment succeeds.", bullet_style))
    story.append(Paragraph("&bull; <b>FR5 &mdash; Seat Tier Pricing:</b> The system shall calculate the total booking cost dynamically based on seat types: SILVER = Rs.150, GOLD = Rs.250, PLATINUM = Rs.400.", bullet_style))
    story.append(Paragraph("&bull; <b>FR6 &mdash; Payment (Standard):</b> Exactly one method (UPI / Card / Cash) per booking. If payment fails, seats are released and booking status becomes FAILED.", bullet_style))
    story.append(Paragraph("&bull; <b>FR7 &mdash; Ticket Generation:</b> Upon successful payment, the system shall format and print an itemized ticket showing Booking ID, Movie, Screen, Start Time, Booked Seats, Total Amount, and Status (CONFIRMED).", bullet_style))
    story.append(Paragraph("&bull; <b>FR8 &mdash; Booking Cancellation:</b> A customer can cancel a booking using its Booking ID, updating status to CANCELLED and restoring seats to AVAILABLE.", bullet_style))

    story.append(Paragraph("<b>Non-Functional Requirements (NFR):</b>", h2_style))
    story.append(Paragraph("&bull; <b>NFR1 &mdash; Modularity:</b> Strict 'one class per file' modularity without external header files.", bullet_style))
    story.append(Paragraph("&bull; <b>NFR2 &mdash; Extensibility (OCP):</b> Adding new payment options (e.g. NetBanking) requires adding a class without modifying existing orchestrator code.", bullet_style))
    story.append(Paragraph("&bull; <b>NFR3 &mdash; Robust Input Validation:</b> Gracefully handles invalid seat IDs (e.g. Z9) and numerical menu strings without crashing.", bullet_style))
    story.append(Paragraph("&bull; <b>NFR4 &mdash; Transactional Rollback:</b> Operations maintain atomic consistency; failed payment rolls back temporary seat locks.", bullet_style))

    story.append(PageBreak())

    # Section 3: Step B
    story.append(Paragraph("3. Step B &mdash; Noun&ndash;Verb Analysis", h1_style))
    noun_data = [
        [Paragraph("Noun Found", table_header), Paragraph("Keep as Class?", table_header), Paragraph("Design Rationale & Justification", table_header)],
        [Paragraph("Movie", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Core entity holding domain data (title, language, duration) and identity.", table_cell)],
        [Paragraph("Seat", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Represents physical chair in auditorium with fixed number and seat tier.", table_cell)],
        [Paragraph("ShowSeat", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("<b>Crucial distinction:</b> Dynamic availability status of a seat for a specific showtime.", table_cell)],
        [Paragraph("Screen", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Auditorium entity that contains and owns physical Seat objects.", table_cell)],
        [Paragraph("Cinema", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Top-level theatre entity that owns auditorium screens.", table_cell)],
        [Paragraph("Show", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Screening entity binding Movie, Screen, and StartTime; owns ShowSeats.", table_cell)],
        [Paragraph("Customer", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Core actor entity holding customer identity (name, phone number).", table_cell)],
        [Paragraph("Booking", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Transactional record encapsulating booking ID, seats, total, and status.", table_cell)],
        [Paragraph("Payment", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Abstract strategy defining the payment contract for runtime polymorphism.", table_cell)],
        [Paragraph("PriceCalculator", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Pure domain calculation service dedicated solely to pricing logic.", table_cell)],
        [Paragraph("TicketPrinter", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Pure presentation service responsible solely for console formatting.", table_cell)],
        [Paragraph("BookingService", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Domain orchestrator managing end-to-end booking workflows and rollback.", table_cell)],
        [Paragraph("SeatCategory", table_cell), Paragraph("<b>Yes</b>", table_cell), Paragraph("Abstract base class for polymorphic tier inspection and statistics.", table_cell)],
        [Paragraph("seat layout", table_cell), Paragraph("<b>No</b>", table_cell), Paragraph("Visual representation view &rarr; encapsulated as method in TicketPrinter.", table_cell)],
        [Paragraph("menu / console", table_cell), Paragraph("<b>No</b>", table_cell), Paragraph("Execution entry point & UI loop &rarr; placed in main.cpp.", table_cell)]
    ]
    t_noun = Table(noun_data, colWidths=[90, 80, 345])
    t_noun.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_noun)

    story.append(Spacer(1, 8))

    # Section 4: Step C
    story.append(Paragraph("4. Step C &mdash; Class Responsibilities & Specifications", h1_style))
    
    # Callout Box: Why ShowSeat
    callout_data = [[
        Paragraph(
            "<b>Architectural Decision: Why ShowSeat and NOT Just Seat?</b><br/>"
            "Physical chair <code>A1</code> exists exactly once in an auditorium (<code>Screen-1</code>). However, its availability status changes for every show: "
            "it may be <b>BOOKED</b> for 06:00 PM and <b>AVAILABLE</b> for 09:00 PM. If status were stored in <code>Seat</code>, booking <code>A1</code> for one show would "
            "incorrectly block it for all shows. Therefore, <code>Seat</code> represents the physical chair, while <code>ShowSeat</code> represents the temporal availability status for a specific <code>Show</code>.",
            table_cell
        )
    ]]
    callout_table = Table(callout_data, colWidths=[515])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3b82f6")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 6))

    class_spec_data = [
        [Paragraph("Class", table_header), Paragraph("Data Members (State)", table_header), Paragraph("Member Methods (Behavior)", table_header), Paragraph("What it MUST NOT Do", table_header)],
        [Paragraph("Movie", table_cell), Paragraph("title, language, durationMinutes", table_cell), Paragraph("getTitle(), getLanguage(), getDurationMinutes()", table_cell), Paragraph("Must NOT know about screens or pricing.", table_cell)],
        [Paragraph("Seat", table_cell), Paragraph("seatNumber, seatType", table_cell), Paragraph("getSeatNumber(), getSeatType(), getTypeName()", table_cell), Paragraph("Must NOT track booking availability.", table_cell)],
        [Paragraph("Screen", table_cell), Paragraph("screenNumber, screenName, seats", table_cell), Paragraph("addSeat(), getSeats(), getScreenNumber()", table_cell), Paragraph("Must NOT manage show scheduling.", table_cell)],
        [Paragraph("Cinema", table_cell), Paragraph("name, screens", table_cell), Paragraph("addScreen(), getScreens(), getScreen()", table_cell), Paragraph("Must NOT process ticket bookings.", table_cell)],
        [Paragraph("Show", table_cell), Paragraph("showId, startTime, movie, screen, showSeats", table_cell), Paragraph("findShowSeat(), bookSeat(), releaseSeat()", table_cell), Paragraph("Must NOT compute monetary totals.", table_cell)],
        [Paragraph("ShowSeat", table_cell), Paragraph("physicalSeat, seatStatus", table_cell), Paragraph("isAvailable(), bookSeat(), releaseSeat()", table_cell), Paragraph("Must NOT create physical chairs.", table_cell)],
        [Paragraph("Customer", table_cell), Paragraph("name, phone", table_cell), Paragraph("getName(), getPhone()", table_cell), Paragraph("Must NOT directly modify seat statuses.", table_cell)],
        [Paragraph("Booking", table_cell), Paragraph("bookingId, customer, show, bookedSeats, totalAmount, status", table_cell), Paragraph("markConfirmed(), markFailed(), markCancelled()", table_cell), Paragraph("Must NOT print console output.", table_cell)],
        [Paragraph("Payment", table_cell), Paragraph("<i>(Pure Virtual Interface)</i>", table_cell), Paragraph("pay(amount) = 0, getPaymentMethodName()", table_cell), Paragraph("Must NOT store booking histories.", table_cell)],
        [Paragraph("PriceCalculator", table_cell), Paragraph("SILVER_PRICE, GOLD_PRICE, PLATINUM_PRICE", table_cell), Paragraph("getPriceForSeatType(), calculateTotal()", table_cell), Paragraph("Must NOT mutate seat availability.", table_cell)],
        [Paragraph("TicketPrinter", table_cell), Paragraph("<i>(Pure Presentation Utility)</i>", table_cell), Paragraph("printTicket(), printSeatLayout()", table_cell), Paragraph("Must NOT mutate business state.", table_cell)],
        [Paragraph("BookingService", table_cell), Paragraph("bookings: vector&lt;Booking&gt;", table_cell), Paragraph("bookTickets(), cancelBooking(), findBooking()", table_cell), Paragraph("Must NOT format UI art.", table_cell)]
    ]
    t_class_spec = Table(class_spec_data, colWidths=[75, 130, 160, 150])
    t_class_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_class_spec)

    story.append(PageBreak())

    # Section 5: Step D
    story.append(Paragraph("5. Step D &mdash; Relationships & Lifetime Test", h1_style))
    rel_data = [
        [Paragraph("Pair", table_header), Paragraph("Relationship", table_header), Paragraph("Lifetime Test & Architectural Justification", table_header)],
        [Paragraph("Cinema &mdash; Screen", table_cell), Paragraph("<b>Composition (&#9670;)</b>", table_cell), Paragraph("<b>YES, the part dies.</b> If Cinema is demolished, all Screen auditoriums inside it cease to exist.", table_cell)],
        [Paragraph("Screen &mdash; Seat", table_cell), Paragraph("<b>Composition (&#9670;)</b>", table_cell), Paragraph("<b>YES, the part dies.</b> Physical seats are bolted to the auditorium floor; destroyed with the Screen.", table_cell)],
        [Paragraph("Show &mdash; Movie", table_cell), Paragraph("<b>Aggregation (&#9671;)</b>", table_cell), Paragraph("<b>NO, the part lives.</b> If a show is cancelled, the Movie entity still exists in the cinema catalogue.", table_cell)],
        [Paragraph("Show &mdash; Screen", table_cell), Paragraph("<b>Aggregation (&#9671;)</b>", table_cell), Paragraph("<b>NO, the part lives.</b> When a show finishes, the Screen auditorium remains intact for other shows.", table_cell)],
        [Paragraph("Show &mdash; ShowSeat", table_cell), Paragraph("<b>Composition (&#9670;)</b>", table_cell), Paragraph("<b>YES, the part dies.</b> ShowSeat is tied to that specific screening slot; dies with the Show.", table_cell)],
        [Paragraph("Booking &mdash; Customer", table_cell), Paragraph("<b>Aggregation (&#9671;)</b>", table_cell), Paragraph("<b>NO, the part lives.</b> Customer profile exists independently of whether a specific booking exists.", table_cell)],
        [Paragraph("Booking &mdash; ShowSeat", table_cell), Paragraph("<b>Aggregation (&#9671;)</b>", table_cell), Paragraph("<b>NO, the part lives.</b> If a Booking is cancelled, ShowSeats remain in the Show (reset to AVAILABLE).", table_cell)],
        [Paragraph("Booking &mdash; Payment", table_cell), Paragraph("<b>Association (&rarr;)</b>", table_cell), Paragraph("<b>Independent lifeline.</b> Booking delegates payment authorization to Payment during checkout.", table_cell)],
        [Paragraph("Payment &mdash; UpiPayment", table_cell), Paragraph("<b>Inheritance (&rArr;)</b>", table_cell), Paragraph("<b>Is-A Relationship.</b> UpiPayment implements the abstract Payment interface.", table_cell)],
        [Paragraph("BookingService &mdash; Booking", table_cell), Paragraph("<b>Aggregation (&#9671;)</b>", table_cell), Paragraph("<b>Maintains collection.</b> BookingService orchestrates and stores confirmed Booking entities.", table_cell)]
    ]
    t_rel = Table(rel_data, colWidths=[120, 105, 290])
    t_rel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_rel)

    story.append(Spacer(1, 8))

    # Section 6: Step E UML Class Diagram
    story.append(Paragraph("6. Step E &mdash; UML Class Diagram", h1_style))
    if class_img and os.path.exists(class_img):
        story.append(Image(class_img, width=515, height=270))
    else:
        story.append(Paragraph("<i>[UML Class Diagram rendered in markdown/report]</i>", body_style))

    story.append(PageBreak())

    # Section 7: Step F UML Sequence Diagram
    story.append(Paragraph("7. Step F &mdash; UML Sequence Diagram", h1_style))
    story.append(Paragraph("<b>Use Case:</b> Customer books 1 seat and pays by UPI (Lifelines: Customer, UI, BookingService, Show, ShowSeat, PriceCalculator, Payment, Booking, TicketPrinter)", body_style))
    if seq_img and os.path.exists(seq_img):
        story.append(Image(seq_img, width=515, height=260))
    else:
        story.append(Paragraph("<i>[UML Sequence Diagram rendered in markdown/report]</i>", body_style))

    story.append(Spacer(1, 8))

    # Section 8: Step G SOLID
    story.append(Paragraph("8. Step G &mdash; SOLID Principles & Intentional Design Non-Goals", h1_style))
    solid_data = [
        [Paragraph("Principle", table_header), Paragraph("How Applied in Codebase", table_header), Paragraph("Concrete Code Location", table_header)],
        [Paragraph("<b>S &mdash; Single Responsibility</b>", table_cell), Paragraph("Each class has one reason to change: PriceCalculator prices; TicketPrinter prints; BookingService orchestrates.", table_cell), Paragraph("11_PriceCalculator.cpp<br/>12_TicketPrinter.cpp", table_cell)],
        [Paragraph("<b>O &mdash; Open/Closed</b>", table_cell), Paragraph("Adding a new payment method (e.g. NetBanking) requires adding a subclass without editing existing code.", table_cell), Paragraph("09_Payment.cpp<br/>10_PaymentTypes.cpp", table_cell)],
        [Paragraph("<b>L &mdash; Liskov Substitution</b>", table_cell), Paragraph("Any derived payment class (UpiPayment, CardPayment) can be passed as Payment* with consistent behavior.", table_cell), Paragraph("10_PaymentTypes.cpp", table_cell)],
        [Paragraph("<b>I &mdash; Interface Segregation</b>", table_cell), Paragraph("Payment interface defines only essential payment contract, avoiding non-universal methods.", table_cell), Paragraph("09_Payment.cpp", table_cell)],
        [Paragraph("<b>D &mdash; Dependency Inversion</b>", table_cell), Paragraph("BookingService depends on abstract Payment* interface rather than concrete payment types.", table_cell), Paragraph("13_BookingService.cpp", table_cell)]
    ]
    t_solid = Table(solid_data, colWidths=[125, 270, 120])
    t_solid.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_solid)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Intentional Design Non-Goals (What Was Deliberately NOT Done):</b>", h2_style))
    story.append(Paragraph("&bull; <b>Deliberately Did NOT Create a Separate `SeatLayout` Class:</b> A seat layout is a visual presentation concern rather than an independent domain entity with its own lifecycle. Encapsulating it in <code>TicketPrinter</code> keeps domain models clean and adheres to High Cohesion.", bullet_style))
    story.append(Paragraph("&bull; <b>Deliberately Did NOT Let `Booking` Own `Payment`:</b> Decoupling payment processors from persistent booking records preserves security and transactional independence.", bullet_style))

    story.append(PageBreak())

    # Section 9: Step H OOP Mapping
    story.append(Paragraph("9. Step H &mdash; OOP Concepts Mapping & Clean Code Checklist", h1_style))
    oop_data = [
        [Paragraph("OOP Concept", table_header), Paragraph("Implementation Details", table_header), Paragraph("Code Reference", table_header)],
        [Paragraph("<b>1. Encapsulation</b>", table_cell), Paragraph("Private attributes; mutation restricted to validated methods (bookSeat, releaseSeat).", table_cell), Paragraph("06_ShowSeat.cpp:24-60<br/>08_Booking.cpp:29-76", table_cell)],
        [Paragraph("<b>2. Abstraction</b>", table_cell), Paragraph("Abstract base class with pure virtual method virtual bool pay(double amount) = 0.", table_cell), Paragraph("09_Payment.cpp:14-22", table_cell)],
        [Paragraph("<b>3. Inheritance</b>", table_cell), Paragraph("UpiPayment, CardPayment, CashPayment inherit from abstract Payment base.", table_cell), Paragraph("10_PaymentTypes.cpp:19", table_cell)],
        [Paragraph("<b>4. Runtime Polymorphism</b>", table_cell), Paragraph("Dynamic method dispatch: payment->pay(totalAmount).", table_cell), Paragraph("13_BookingService.cpp:91", table_cell)],
        [Paragraph("<b>5. Compile-Time Polymorphism</b>", table_cell), Paragraph("Overloaded constructors and overloaded PriceCalculator::calculateTotal() methods.", table_cell), Paragraph("11_PriceCalculator.cpp:33-46", table_cell)],
        [Paragraph("<b>6. Static Members</b>", table_cell), Paragraph("Class-level static counter static int nextBookingId generating unique IDs (BK1001).", table_cell), Paragraph("08_Booking.cpp:30-46", table_cell)],
        [Paragraph("<b>7. 'this' Keyword</b>", table_cell), Paragraph("Used to disambiguate member variables from parameters and refer to calling object.", table_cell), Paragraph("01_Movie.cpp, 07_Customer.cpp", table_cell)],
        [Paragraph("<b>8. Composition</b>", table_cell), Paragraph("Cinema owns Screen; Screen owns Seat; Show owns ShowSeat.", table_cell), Paragraph("03_Screen.cpp, 04_Cinema.cpp", table_cell)],
        [Paragraph("<b>9. Aggregation</b>", table_cell), Paragraph("Show references Movie & Screen; Booking references Customer & ShowSeats.", table_cell), Paragraph("05_Show.cpp, 08_Booking.cpp", table_cell)],
        [Paragraph("<b>10. Association</b>", table_cell), Paragraph("Customer interacts with BookingService to book tickets; neither owns the other.", table_cell), Paragraph("13_BookingService.cpp:69-74", table_cell)]
    ]
    t_oop = Table(oop_data, colWidths=[130, 260, 125])
    t_oop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_oop)

    story.append(Spacer(1, 8))

    # Section 10: Step I Test Results
    story.append(Paragraph("10. Step I &mdash; Automated Verification Test Suite Execution", h1_style))
    test_output_text = """======================================================
  RUNNING OPTIMIZED AUTOMATED VERIFICATION SUITE      
======================================================

Screen-1  06:00 PM |  3 Idiots
SILVER     A1[ ] A2[X] A3[ ] A4[ ] 
GOLD       B1[ ] B2[ ] B3[X] 
PLATINUM   C1[ ] C2[ ] 

Selected Seats Breakdown:
  A1   SILVER    Rs.150
  B2   GOLD      Rs.250
  TOTAL     Rs.400

[UPI] Rs.400 paid successfully

================ TICKET ================
Booking ID : BK1001
Movie      : 3 Idiots
Screen     : Screen-1   06:00 PM
Seats      : A1, B2
Amount     : Rs.400     Status: CONFIRMED
========================================

>> TEST 1 PASSED: Confirmed ID BK1001
[Booking Rejected] Seat A1 is already BOOKED. No seats reserved.
>> TEST 2 PASSED: Double booking rejected; A3 remains AVAILABLE.

Selected Seats Breakdown:
  A3   SILVER    Rs.150
  TOTAL     Rs.150

[Card] Transaction FAILED: Insufficient balance / Card declined.
[Booking Failed] Payment was not successful. Seats have been released.
>> TEST 3 PASSED: Payment failure rolled back; A3 remains AVAILABLE.
[Success] Booking BK1001 has been cancelled. Seats are now AVAILABLE.
>> TEST 4 PASSED: Booking cancelled; seats A1 & B2 released.
[Booking Rejected] Seat Z9 does not exist.
>> TEST 5 PASSED: Invalid seat handled without crash.

======================================================
        ALL OPTIMIZED TESTS PASSED SUCCESSFULLY       
======================================================
"""
    raw_lines = [Paragraph(f"<code>{line}</code>", code_style) for line in test_output_text.split("\n")]
    raw_table_data = [[line] for line in raw_lines]
    t_test = Table(raw_table_data, colWidths=[515])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('PADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t_test)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF successfully: {output_filename}")

if __name__ == "__main__":
    build_pdf()
