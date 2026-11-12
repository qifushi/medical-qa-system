interface User {
  /**
   * 用户id
   */
  id: string
  /**
   * 用户名
   */
  username: string
  /**
   * 邮箱
   */
  email: string
  /**
   * 用户角色
   */
  role: string
  /**
   * 用户权限
   */
  permissions: Array<string>
  /**
   * 是否需要修改密码
   */
  is_edit_password?: boolean
    /**
   * 应用主题色
   */
    app_theme_color:string
    /**
     * 手机号码
     */
    phone?:string
    /**
     * 姓名
     */
    nick_name?:string
}

interface LoginRequest {
  /**
   * 用户名
   */
  username: string
  /**
   * 密码
   */
  password: string
}

interface RegisterRequest {
  /**
   * 用户名
   */
  username: string
  /**
   * 密码
   */
  password: string
  /**
   * 确定密码
   */
  re_password: string
  /**
   * 邮箱
   */
  email: string
  /**
   * 验证码
   */
  code: string
}

interface CheckCodeRequest {
  /**
   * 邮箱
   */
  email: string
  /**
   *验证码
   */
  code: string
  /**
   * 类型
   */
  type: 'register' | 'reset_password'
}

interface ResetCurrentUserPasswordRequest {
  /**
   * 验证码
   */
  code: string
  /**
   *密码
   */
  password: string
  /**
   * 确认密码
   */
  re_password: string
}

interface ResetPasswordRequest {
  /**
   * 邮箱
   */
  email?: string
  /**
   * 验证码
   */
  code?: string
  /**
   * 密码
   */
  password: string
  /**
   * 确认密码
   */
  re_password: string
}

export type {
  CheckCodeRequest, LoginRequest,
  RegisterRequest, ResetCurrentUserPasswordRequest, ResetPasswordRequest,
  User
}

