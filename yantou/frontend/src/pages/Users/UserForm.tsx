/**
 * 用户创建/编辑表单
 */
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Modal, Form, Input, Switch, Select, DatePicker, message, Row, Col } from 'antd'
import { createUser, updateUser, getUserDetail } from '@/api/user'
import { getDepartmentList } from '@/api/department'
import { useDebounceFn } from '@/hooks/useDebounce'
import type { UserListItem, CreateUserRequest, UpdateUserRequest } from '@/types/user'
import type { DepartmentListItem } from '@/types/department'
import dayjs from 'dayjs'

interface UserFormProps {
  visible: boolean
  user: UserListItem | null
  onClose: () => void
  onSuccess: () => void
}

const UserForm = ({ visible, user, onClose, onSuccess }: UserFormProps) => {
  const { t } = useTranslation()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [departmentOptions, setDepartmentOptions] = useState<Array<{ label: string; value: number }>>([])
  const [loadingDepartments, setLoadingDepartments] = useState(false)

  // 加载部门选项
  const loadDepartmentOptions = async () => {
    setLoadingDepartments(true)
    try {
      const response = await getDepartmentList({ page_size: 1000, is_active: true })
      const options = response.results.map((dept) => ({
        label: dept.name,
        value: dept.id,
      }))
      setDepartmentOptions([{ label: t('user.noDepartment') || '无', value: 0 }, ...options])
    } catch (error: any) {
      message.error(error.message || '加载部门列表失败')
    } finally {
      setLoadingDepartments(false)
    }
  }

  // 加载用户详情（编辑模式）
  const loadUserDetail = async (userId: number) => {
    try {
      const userDetail = await getUserDetail(userId)
      form.setFieldsValue({
        username: userDetail.username,
        email: userDetail.email,
        phone: userDetail.phone || userDetail.profile?.phone,
        first_name: userDetail.first_name,
        last_name: userDetail.last_name,
        is_active: userDetail.is_active,
        is_staff: userDetail.is_staff,
        department: userDetail.profile?.department || 0,
        position: userDetail.profile?.position,
        employee_no: userDetail.profile?.employee_no,
        gender: userDetail.profile?.gender,
        birthday: userDetail.profile?.birthday ? dayjs(userDetail.profile.birthday) : null,
        address: userDetail.profile?.address,
        bio: userDetail.profile?.bio,
        join_date: userDetail.profile?.join_date ? dayjs(userDetail.profile.join_date) : null,
      })
    } catch (error: any) {
      message.error(error.message || '加载用户详情失败')
    }
  }

  // 初始化表单
  useEffect(() => {
    if (visible) {
      if (user) {
        // 编辑模式：加载用户详情
        loadUserDetail(user.id)
      } else {
        // 创建模式：重置表单
        form.resetFields()
        form.setFieldsValue({
          is_active: true,
          is_staff: false,
          department: 0,
        })
      }
      
      // 加载部门选项
      loadDepartmentOptions()
    }
  }, [visible, user, form])

  // 处理提交（实际执行函数）
  const executeSubmit = async () => {
    try {
      const values = await form.validateFields()
      setLoading(true)

      if (user) {
        // 更新用户
        const phone = values.phone?.trim() || undefined
        const formData: UpdateUserRequest = {
          email: values.email,
          phone: phone,
          first_name: values.first_name?.trim() || undefined,
          last_name: values.last_name?.trim() || undefined,
          is_active: values.is_active,
          is_staff: values.is_staff,
          profile: {
            phone: phone,
            department: values.department === 0 ? undefined : values.department,
            position: values.position?.trim() || undefined,
            employee_no: values.employee_no?.trim() || undefined,
            gender: values.gender,
            birthday: values.birthday ? values.birthday.format('YYYY-MM-DD') : undefined,
            address: values.address?.trim() || undefined,
            bio: values.bio?.trim() || undefined,
            join_date: values.join_date ? values.join_date.format('YYYY-MM-DD') : undefined,
          },
        }
        await updateUser(user.id, formData)
        message.success(t('user.updateSuccess') || '用户更新成功')
      } else {
        // 创建用户
        const phone = values.phone?.trim() || undefined
        const formData: CreateUserRequest = {
          username: values.username,
          email: values.email,
          password: values.password,
          password_confirm: values.password_confirm,
          phone: phone,
          first_name: values.first_name?.trim() || undefined,
          last_name: values.last_name?.trim() || undefined,
          is_active: values.is_active !== undefined ? values.is_active : true,
          is_staff: values.is_staff || false,
          profile: {
            phone: phone,
            department: values.department === 0 ? undefined : values.department,
            position: values.position?.trim() || undefined,
            employee_no: values.employee_no?.trim() || undefined,
            gender: values.gender,
            birthday: values.birthday ? values.birthday.format('YYYY-MM-DD') : undefined,
            address: values.address?.trim() || undefined,
            bio: values.bio?.trim() || undefined,
            join_date: values.join_date ? values.join_date.format('YYYY-MM-DD') : undefined,
          },
        }
        await createUser(formData)
        message.success(t('user.createSuccess') || '用户创建成功')
      }

      onSuccess()
    } catch (error: any) {
      if (error?.errorFields) {
        // 表单验证错误
        return
      }
      message.error(error.message || (user ? '更新用户失败' : '创建用户失败'))
    } finally {
      setLoading(false)
    }
  }

  // 防抖处理提交（防止重复点击）
  const handleSubmitDebounced = useDebounceFn(executeSubmit, 500)

  const handleSubmit = () => {
    // 如果正在加载，不执行（防止重复提交）
    if (loading) {
      return
    }
    // 使用防抖，防止快速连续点击
    handleSubmitDebounced()
  }

  // 处理取消
  const handleCancel = () => {
    form.resetFields()
    onClose()
  }

  return (
    <Modal
      title={user ? (t('user.edit') || '编辑用户') : (t('user.create') || '创建用户')}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      confirmLoading={loading}
      width={800}
      destroyOnClose
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          is_active: true,
          is_staff: false,
          department: 0,
        }}
      >
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="username"
              label={t('user.username') || '用户名'}
              rules={[
                { required: !user, message: t('user.usernameRequired') || '请输入用户名' },
                { min: 3, message: t('user.usernameMinLength') || '用户名至少3个字符' },
                { max: 30, message: t('user.usernameMaxLength') || '用户名不能超过30个字符' },
              ]}
            >
              <Input 
                placeholder={t('user.usernamePlaceholder') || '请输入用户名'} 
                disabled={!!user}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="email"
              label={t('user.email') || '邮箱'}
              rules={[
                { required: true, message: t('user.emailRequired') || '请输入邮箱' },
                { type: 'email', message: t('user.emailInvalid') || '请输入有效的邮箱地址' },
              ]}
            >
              <Input placeholder={t('user.emailPlaceholder') || '请输入邮箱'} />
            </Form.Item>
          </Col>
        </Row>

        {!user && (
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="password"
                label={t('user.password') || '密码'}
                rules={[
                  { required: true, message: t('user.passwordRequired') || '请输入密码' },
                  { min: 8, message: t('user.passwordMinLength') || '密码至少8个字符' },
                ]}
              >
                <Input.Password placeholder={t('user.passwordPlaceholder') || '请输入密码'} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="password_confirm"
                label={t('user.passwordConfirm') || '确认密码'}
                dependencies={['password']}
                rules={[
                  { required: true, message: t('user.passwordConfirmRequired') || '请确认密码' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('password') === value) {
                        return Promise.resolve()
                      }
                      return Promise.reject(new Error(t('user.passwordMismatch') || '两次输入的密码不一致'))
                    },
                  }),
                ]}
              >
                <Input.Password placeholder={t('user.passwordConfirmPlaceholder') || '请再次输入密码'} />
              </Form.Item>
            </Col>
          </Row>
        )}

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="first_name"
              label={t('user.firstName') || '名'}
              rules={[
                { max: 30, message: t('user.nameMaxLength') || '姓名不能超过30个字符' },
              ]}
            >
              <Input placeholder={t('user.firstNamePlaceholder') || '请输入名'} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="last_name"
              label={t('user.lastName') || '姓'}
              rules={[
                { max: 30, message: t('user.nameMaxLength') || '姓名不能超过30个字符' },
              ]}
            >
              <Input placeholder={t('user.lastNamePlaceholder') || '请输入姓'} />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="phone"
              label={t('user.phone') || '手机号'}
              rules={[
                { pattern: /^1[3-9]\d{9}$/, message: t('user.phoneInvalid') || '请输入有效的手机号' },
              ]}
            >
              <Input placeholder={t('user.phonePlaceholder') || '请输入手机号'} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="department"
              label={t('user.department') || '部门'}
            >
              <Select
                placeholder={t('user.departmentPlaceholder') || '请选择部门'}
                loading={loadingDepartments}
                allowClear
                showSearch
                filterOption={(input, option) =>
                  (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                }
                options={departmentOptions}
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="position"
              label={t('user.position') || '职位'}
              rules={[
                { max: 100, message: t('user.positionMaxLength') || '职位不能超过100个字符' },
              ]}
            >
              <Input placeholder={t('user.positionPlaceholder') || '请输入职位'} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="employee_no"
              label={t('user.employeeNo') || '工号'}
              rules={[
                { max: 50, message: t('user.employeeNoMaxLength') || '工号不能超过50个字符' },
              ]}
            >
              <Input placeholder={t('user.employeeNoPlaceholder') || '请输入工号'} />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="gender"
              label={t('user.gender') || '性别'}
            >
              <Select
                placeholder={t('user.genderPlaceholder') || '请选择性别'}
                options={[
                  { label: t('user.genderUnknown') || '未知', value: 0 },
                  { label: t('user.genderMale') || '男', value: 1 },
                  { label: t('user.genderFemale') || '女', value: 2 },
                ]}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="birthday"
              label={t('user.birthday') || '生日'}
            >
              <DatePicker
                style={{ width: '100%' }}
                placeholder={t('user.birthdayPlaceholder') || '请选择生日'}
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="join_date"
              label={t('user.joinDate') || '入职日期'}
            >
              <DatePicker
                style={{ width: '100%' }}
                placeholder={t('user.joinDatePlaceholder') || '请选择入职日期'}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="address"
              label={t('user.address') || '地址'}
              rules={[
                { max: 500, message: t('user.addressMaxLength') || '地址不能超过500个字符' },
              ]}
            >
              <Input placeholder={t('user.addressPlaceholder') || '请输入地址'} />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          name="bio"
          label={t('user.bio') || '个人简介'}
          rules={[
            { max: 500, message: t('user.bioMaxLength') || '个人简介不能超过500个字符' },
          ]}
        >
          <Input.TextArea
            rows={3}
            placeholder={t('user.bioPlaceholder') || '请输入个人简介'}
          />
        </Form.Item>

        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="is_active"
              label={t('user.status') || '状态'}
              valuePropName="checked"
            >
              <Switch checkedChildren={t('common.active') || '激活'} unCheckedChildren={t('common.inactive') || '禁用'} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="is_staff"
              label={t('user.isStaff') || '员工'}
              valuePropName="checked"
            >
              <Switch checkedChildren={t('common.yes') || '是'} unCheckedChildren={t('common.no') || '否'} />
            </Form.Item>
          </Col>
        </Row>
      </Form>
    </Modal>
  )
}

export default UserForm

