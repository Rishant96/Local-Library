from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the url
# patterns
import uuid


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=140, help_text='Enter a book genre '
                            '(e.g. Science Fiction)')

    def __str__(self):
        """Human-friendly represention of the genre of a book."""
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""

    title = models.CharField(max_length=200)

    # Foreign Key used because a book can only have one author, but
    # an author can have multiple books.
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief '
                               'description of the book')

    isbn = models.CharField('ISBN', max_length=13, help_text='13 character '
                            '<a href="https://www.isbn-international.org/'
                            'content/what-isbn">ISBN number</a>')

    # ManyToManyField used because a genre can contain many books. While, a
    # book can belong to many genres.
    genre = models.ManyToManyField(Genre, help_text='Select a genre'
                                   'for this book')

    def __str__(self):
        """Human-friendly representation of a book."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access the details view of this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (that can be borrowed
       from the library)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Uni'
                          'que ID for this particular book across the whole '
                          'library.')

    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
            ('m', 'Maintenance'),
            ('o', 'On Loan'),
            ('a', 'Available'),
            ('r', 'Reserved')
        )

    status = models.CharField(
            max_length=1,
            choices=LOAN_STATUS,
            blank=True,
            default='m',
            help_text='Book Availability',
        )

    def __str__(self):
        """Human-friendly representation of a book instance."""
        return f'{self.id} : {self.book.title}'

    class Meta:
        ordering = ['due_back']
