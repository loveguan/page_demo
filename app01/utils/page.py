"""
自定义分页组件

"""


class Pagination(object):

    def __init__(self, data_num, current_page, url_prefix, params, per_page=10, max_show=3):
        """
        进行初始化.
        :param data_num: 数据总数
        :param current_page: 当前页
        :param url_prefix: 生成的页码的链接前缀
        :param per_page: 每页显示多少条数据
        :param max_show: 页面最多显示多少个页码
        """
        self.data_num = data_num
        self.per_page = per_page
        self.max_show = max_show
        self.url_prefix = url_prefix

        # 把页码数算出来
        self.page_num, more = divmod(data_num, per_page)
        if more:
            self.page_num += 1

        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
            # 如果URL传过来的页码数是负数
        if self.current_page <= 0:
            self.current_page = 1
            # 如果URL传过来的页码数超过了最大页码数
        elif self.current_page > self.page_num:
            self.current_page = self.page_num  # 默认展示最后一页

        # 页码数的一半 算出来
        self.half_show = max_show // 2

        # 页码最左边显示多少
        if self.current_page - self.half_show <= 1:
            self.page_start = 1
            self.page_end = self.max_show
        elif self.current_page + self.half_show >= self.page_num:  # 如果右边越界
            self.page_end = self.page_num
            self.page_start = self.page_num - self.max_show
        else:
            self.page_start = self.current_page - self.half_show
            # 页码最右边显示
            self.page_end = self.current_page + self.half_show

        import copy
        self.params = copy.deepcopy(params)  # {"page":"12","title_startwith":"py","id__gt":"5"}

    @property
    def start(self):
        # 数据从哪儿开始切
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        # 数据切片切到哪儿
        return self.current_page * self.per_page

    def page_html(self):
        # 生成页码
        l = []
        # 加一个首页
        self.params["page"] = 1

        l.append('<li><a href="{0}?{1}">首页</a></li>'.format(self.url_prefix,self.params.urlencode()))
        # 加一个上一页
        if self.current_page == 1:
            l.append('<li class="disabled" ><a href="#">«</a></li>'.format(self.current_page))
        else:
            self.params["page"] = self.current_page - 1
            l.append('<li><a href="{0}?{1}">«</a></li>'.format(self.url_prefix, self.params.urlencode()))

        # {"page":"12","title_startwith":"py","id__gt":"5"}  #  "page=12&title_startwith=py&id__gt=5"

        print(self.params.urlencode())
        for i in range(self.page_start, self.page_end + 1):
            # 选择新的页码时候，只替换页码保留后面的查询条件
            self.params["page"] = i  # # {"page":"7","title_startwith":"py","id__gt":"5"}  #  "page=7&title_startwith=py&id__gt=5"
            if i == self.current_page:
                tmp = '<li class="active"><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix, self.params.urlencode(), i)
            else:
                tmp = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix, self.params.urlencode(), i)
            l.append(tmp)

        # 加一个下一页
        if self.current_page == self.page_num:
            l.append('<li class="disabled"><a href="#">»</a></li>'.format(self.current_page))
        else:
            self.params["page"] =self.current_page + 1
            l.append('<li><a href="{0}?{1}">»</a></li>'.format(self.url_prefix, self.params.urlencode()))
        # 加一个尾页,将页码指向最后
        self.params["page"] = self.page_num
        l.append('<li><a href="{0}?{1}">尾页</a></li>'.format(self.url_prefix, self.params.urlencode()))
        return "".join(l)
