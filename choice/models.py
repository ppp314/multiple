'''
    Multiple is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Multiple.  If not, see <https://www.gnu.org/licenses/>.
'''


from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.forms.formsets import formset_factory, BaseFormSet
from django import forms


class Exam(models.Model):

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name='テスト名',
        max_length=200
        )

    created_date = models.DateTimeField(
        verbose_name='作成日',
        default=timezone.now
        )

    number_of_question = models.IntegerField(
        verbose_name='問題数',
        default=1
        )

    class Meta:

        verbose_name = '試験'
        verbose_name_plural = '試験'
        ordering = ['pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('choice:question-index', kwargs={'pk': self.pk})


class Question(models.Model):

    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)

    no = models.IntegerField(
        verbose_name='大問',
        default=0
        )

    sub_no = models.IntegerField(
        verbose_name='小問',
        default=0
        )

    point = models.IntegerField(
        verbose_name='配点',
        default=0
        )

    choice1 = models.BooleanField(null=False, default=False)
    choice2 = models.BooleanField(null=False, default=False)
    choice3 = models.BooleanField(null=False, default=False)
    choice4 = models.BooleanField(null=False, default=False)
    choice5 = models.BooleanField(null=False, default=False)

    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'
        ordering = ['pk']

    def __str__(self):
        return str(self.no) + '-' + str(self.sub_no)


class BookmarkForm(forms.Form):
    title = forms.CharField(max_length=100)
    url = forms.CharField(max_length=100)


class BaseBookmarkFormSet(BaseFormSet):
    def clean(self):
        url_list = [form['url'].value() for form in self.forms]

        if len(url_list) > len(set(url_list)):
            raise forms.ValidationError("duplicate url")


BookmarkFormSet = formset_factory(BookmarkForm, formset=BaseBookmarkFormSet, extra=1, max_num=100)


class Question2Form(forms.Form):
    class Meta:
        model = Question
        fields = ('no', 'sub_no', 'choice1', 'choice2', 'choice3', 'choice4', 'choice5')


QuestionFormSet = formset_factory(Question2Form, formset=BaseFormSet, extra=2, max_num=10)
